#!/usr/bin/env python3
"""Install missing TeX packages required by Beautybook/Quarto build."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

SCAN_FILES = [
    ROOT / "beautybook.cls",
    *sorted((ROOT / "stys").glob("*.sty")),
    *sorted((ROOT / "include").glob("*.tex")),
]

index_tex = ROOT / "index.tex"
if index_tex.exists():
    SCAN_FILES.append(index_tex)

# Recent render logs (optional) for missing-file detection
LOG_FILES = [ROOT / "index.log"]

PKG_RE = re.compile(r"\\(?:RequirePackage|usepackage)(?:\[[^\]]*\])?\{([^}]+)\}(?:\[[^\]]*\])?")
TIKZ_RE = re.compile(r"\\usetikzlibrary\{([^}]+)\}")

OPTIONAL_PACKAGES = {"mtpro2"}


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=False, text=True, capture_output=True)

def can_write_dir(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        test_file = path / ".codex_write_test"
        test_file.write_text("ok", encoding="utf-8")
        test_file.unlink()
        return True
    except Exception:
        return False


def find_tlmgr() -> str:
    env_path = os.environ.get("TLMGR")
    if env_path and Path(env_path).exists():
        return env_path

    tinytex = Path.home() / ".TinyTeX" / "bin"
    if tinytex.exists():
        candidates = list(tinytex.glob("*/tlmgr"))
        if candidates:
            return str(candidates[0])

    return "tlmgr"


def find_kpsewhich() -> str:
    env_path = os.environ.get("KPSEWHICH")
    if env_path and Path(env_path).exists():
        return env_path

    tinytex = Path.home() / ".TinyTeX" / "bin"
    if tinytex.exists():
        candidates = list(tinytex.glob("*/kpsewhich"))
        if candidates:
            return str(candidates[0])

    return "kpsewhich"


def kpsewhich(file: str) -> bool:
    kps = find_kpsewhich()
    res = run([kps, file])
    return bool(res.stdout.strip())


def parse_packages(files: Iterable[Path]) -> tuple[set[str], set[str]]:
    packages: set[str] = set()
    tikz_libs: set[str] = set()
    for path in files:
        try:
            text = path.read_text(errors="ignore")
        except Exception:
            continue
        for m in PKG_RE.finditer(text):
            for name in m.group(1).split(","):
                name = name.strip()
                if not name:
                    continue
                if name.startswith("stys/"):
                    continue
                packages.add(name)
        for m in TIKZ_RE.finditer(text):
            for lib in m.group(1).split(","):
                lib = lib.strip()
                if lib:
                    tikz_libs.add(lib)
    return packages, tikz_libs


def wants_emoji_font(files: Iterable[Path]) -> bool:
    for path in files:
        try:
            text = path.read_text(errors="ignore")
        except Exception:
            continue
        if "Noto Color Emoji" in text:
            return True
    return False


def tlmgr_search(tlmgr_cmd: list[str], filename: str) -> set[str]:
    res = run([*tlmgr_cmd, "search", "--file", "--global", f"/{filename}"])
    pkgs: set[str] = set()
    for line in res.stdout.splitlines():
        if line.endswith(":"):
            pkgs.add(line[:-1])
    return pkgs


def main() -> int:
    tlmgr = find_tlmgr()
    tlmgr_cmd = [tlmgr]

    # Fallback to user mode if the TinyTeX tree is not writable (common on shared systems)
    tlpkg_dir = Path.home() / ".TinyTeX" / "tlpkg"
    if tlpkg_dir.exists() and not can_write_dir(tlpkg_dir):
        texmf_home = ROOT / ".texmf"
        texmf_var = ROOT / ".texmf-var"
        texmf_config = ROOT / ".texmf-config"
        texmf_home.mkdir(parents=True, exist_ok=True)
        texmf_var.mkdir(parents=True, exist_ok=True)
        texmf_config.mkdir(parents=True, exist_ok=True)
        os.environ["TEXMFHOME"] = str(texmf_home)
        os.environ["TEXMFVAR"] = str(texmf_var)
        os.environ["TEXMFCONFIG"] = str(texmf_config)
        tlmgr_cmd = [tlmgr, "--usermode"]
        run([*tlmgr_cmd, "init-usertree"])

    packages, tikz_libs = parse_packages(SCAN_FILES)
    packages -= OPTIONAL_PACKAGES
    needs_emoji_font = wants_emoji_font(SCAN_FILES)

    missing_files: list[str] = []
    for pkg in sorted(packages):
        sty = f"{pkg}.sty" if not pkg.endswith(".sty") else pkg
        if not kpsewhich(sty):
            missing_files.append(sty)

    for lib in sorted(tikz_libs):
        if kpsewhich(f"tikzlibrary{lib}.code.tex"):
            continue
        if kpsewhich(f"pgflibrary{lib}.code.tex"):
            continue
        missing_files.append(f"tikzlibrary{lib}.code.tex")

    if needs_emoji_font:
        if not (kpsewhich("NotoColorEmoji.ttf") or kpsewhich("NotoColorEmoji.otf")):
            missing_files.append("NotoColorEmoji.ttf")

    # Parse log files for missing files not directly referenced (transitive deps)
    missing_re = re.compile(r"File `([^']+)' not found")
    missing_font_re = re.compile(r"I can't find file `([^']+)'")
    for log in LOG_FILES:
        if not log.exists():
            continue
        try:
            text = log.read_text(errors="ignore")
        except Exception:
            continue
        for m in missing_re.finditer(text):
            missing_files.append(m.group(1))
        for m in missing_font_re.finditer(text):
            name = m.group(1)
            # Try common font file extensions
            if "." in name:
                missing_files.append(name)
            else:
                missing_files.extend([f"{name}.tfm", f"{name}.otf", f"{name}.ttf"])

    if not missing_files:
        print("All TeX packages appear to be available.")
        return 0

    pkgs_to_install: set[str] = set()
    for mf in missing_files:
        found = tlmgr_search(tlmgr_cmd, mf)
        if not found:
            print(f"WARN: no tlmgr package found for {mf}")
            continue
        pkgs_to_install.update(found)

    if not pkgs_to_install:
        print("No installable packages were found for missing files.")
        return 1

    cmd = [*tlmgr_cmd, "install", *sorted(pkgs_to_install)]
    print("Installing:", " ".join(sorted(pkgs_to_install)))
    res = run(cmd)
    print(res.stdout)
    if res.returncode != 0:
        print(res.stderr)
    return res.returncode


if __name__ == "__main__":
    raise SystemExit(main())
