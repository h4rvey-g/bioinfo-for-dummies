#!/usr/bin/env bash
set -euo pipefail

quarto_version="$(
  curl -fsSL https://api.github.com/repos/quarto-dev/quarto-cli/releases/latest \
    | python -c "import json,sys; print(json.load(sys.stdin)['tag_name'].lstrip('v'))"
)"

curl -fsSL -o /tmp/quarto.tgz \
  "https://github.com/quarto-dev/quarto-cli/releases/download/v${quarto_version}/quarto-${quarto_version}-linux-amd64.tar.gz"
tar -xzf /tmp/quarto.tgz -C /tmp

"/tmp/quarto-${quarto_version}/bin/quarto" render --to html
python scripts/generate_sitemap.py --base-url https://b4d.h4rvey.com
