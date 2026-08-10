#!/usr/bin/env python3
"""Copy the bundled report template and set its basic metadata."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


ACCENT_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="Directory to create or update")
    parser.add_argument("--title", default="Dynamic system evidence report")
    parser.add_argument("--brand", default="Technical Report")
    parser.add_argument("--accent", default="#39BF5E")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite template-owned files in an existing directory without deleting unrelated files",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not ACCENT_PATTERN.fullmatch(args.accent):
        raise SystemExit("--accent must be a six-digit hex color such as #39BF5E")

    template = Path(__file__).resolve().parents[1] / "assets" / "report-template"
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()) and not args.force:
        raise SystemExit(f"Output is not empty: {output}. Pass --force to overwrite template-owned files.")

    output.mkdir(parents=True, exist_ok=True)
    shutil.copytree(template, output, dirs_exist_ok=True)

    config_path = output / "data" / "report-config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["title"] = args.title
    config["brand"] = args.brand
    config["accent"] = args.accent.upper()
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")

    print(f"Created technical report: {output}")
    print(f"Serve with: python -m http.server 8010 --directory \"{output}\"")


if __name__ == "__main__":
    main()

