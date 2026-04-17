#!/usr/bin/env bash
set -euo pipefail

python_bin="python"
if [ -x ".venv/bin/python" ]; then
  python_bin=".venv/bin/python"
  export PATH="$(pwd)/.venv/bin:${PATH}"
fi

quarto_version="$(
  curl -fsSL https://api.github.com/repos/quarto-dev/quarto-cli/releases/latest \
    | "$python_bin" -c "import json,sys; print(json.load(sys.stdin)['tag_name'].lstrip('v'))"
)"

curl -fsSL -o /tmp/quarto.tgz \
  "https://github.com/quarto-dev/quarto-cli/releases/download/v${quarto_version}/quarto-${quarto_version}-linux-amd64.tar.gz"
tar -xzf /tmp/quarto.tgz -C /tmp

"/tmp/quarto-${quarto_version}/bin/quarto" render --to html
"$python_bin" scripts/generate_sitemap.py --base-url https://b4d.h4rvey.com
