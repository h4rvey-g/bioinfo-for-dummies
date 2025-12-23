#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
from urllib.parse import urljoin


EXCLUDE_DIRS = {"site_libs"}


def iter_html_files(root: Path) -> list[Path]:
    html_files: list[Path] = []
    for path in root.rglob("*.html"):
        if path.is_dir():
            continue
        rel = path.relative_to(root)
        parts = rel.parts
        if any(part.startswith(".") for part in parts):
            continue
        if any(part in EXCLUDE_DIRS for part in parts):
            continue
        html_files.append(path)
    return sorted(html_files, key=lambda p: p.as_posix())


def build_sitemap(base_url: str, output_dir: Path, output_path: Path) -> None:
    base_url = base_url.rstrip("/") + "/"
    files = iter_html_files(output_dir)
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for f in files:
        rel = f.relative_to(output_dir).as_posix()
        loc = urljoin(base_url, rel)
        lastmod = dt.datetime.fromtimestamp(f.stat().st_mtime).date().isoformat()
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate sitemap.xml for Quarto book output.")
    parser.add_argument(
        "--base-url",
        required=True,
        help="Base URL of the deployed site, e.g. https://b4d.h4rvey.com",
    )
    parser.add_argument(
        "--output-dir",
        default="_book",
        help="Quarto output directory containing HTML files (default: _book)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output sitemap.xml path (default: <output-dir>/sitemap.xml)",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    if not output_dir.exists():
        raise SystemExit(f"Output directory not found: {output_dir}")

    output_path = Path(args.output) if args.output else output_dir / "sitemap.xml"
    build_sitemap(args.base_url, output_dir, output_path)
    print(f"Wrote sitemap: {output_path}")


if __name__ == "__main__":
    main()
