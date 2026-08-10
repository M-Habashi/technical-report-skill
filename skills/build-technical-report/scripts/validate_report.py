#!/usr/bin/env python3
"""Validate the static structure of a generated technical report."""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path


REQUIRED_FILES = (
    "index.html",
    "data/report-config.json",
    "scripts/main.js",
    "scripts/app-shell.js",
    "scripts/interactive-plot.js",
    "styles/base.css",
    "styles/content.css",
    "styles/plots.css",
    "styles/responsive.css",
)


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.internal_links: list[str] = []
        self.article_ids: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            self.ids.append(element_id)
        href = values.get("href")
        if href and href.startswith("#") and len(href) > 1:
            self.internal_links.append(href[1:])
        classes = set((values.get("class") or "").split())
        if tag == "article" and "report-article" in classes and element_id:
            self.article_ids.append(element_id)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    return parser.parse_args()


def fail(errors: list[str]) -> None:
    print("Report validation failed:")
    for error in errors:
        print(f"  - {error}")
    raise SystemExit(1)


def main() -> None:
    root = parse_args().report.resolve()
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    config_path = root / "data" / "report-config.json"
    if not config_path.is_file():
        fail(errors)

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        errors.append(f"invalid report-config.json: {exc}")
        fail(errors)

    articles = config.get("articles")
    if not isinstance(articles, list) or not articles:
        errors.append("report-config.json must contain a non-empty articles array")
        fail(errors)

    accent = config.get("accent", "")
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", accent):
        errors.append("accent must be a six-digit hex color")

    configured_ids: list[str] = []
    all_ids: list[str] = []
    all_links: list[str] = []
    parsed_article_ids: list[str] = []
    component_paths: set[str] = set()

    for index, article in enumerate(articles, start=1):
        if not isinstance(article, dict):
            errors.append(f"article {index} is not an object")
            continue
        missing = [key for key in ("id", "label", "summary", "component") if not article.get(key)]
        if missing:
            errors.append(f"article {index} is missing: {', '.join(missing)}")
            continue

        article_id = article["id"]
        component = article["component"]
        configured_ids.append(article_id)
        if not re.fullmatch(r"article-[1-9][0-9]*", article_id):
            errors.append(f"invalid article id: {article_id}")
        if component in component_paths:
            errors.append(f"component registered more than once: {component}")
        component_paths.add(component)

        component_path = root / component
        if not component_path.is_file():
            errors.append(f"missing article component: {component}")
            continue

        source = component_path.read_text(encoding="utf-8")
        if "TODO" in source or "{{" in source:
            errors.append(f"placeholder content remains in {component}")
        parser = StructureParser()
        parser.feed(source)
        all_ids.extend(parser.ids)
        all_links.extend(parser.internal_links)
        parsed_article_ids.extend(parser.article_ids)
        if article_id not in parser.article_ids:
            errors.append(f"{component} does not contain report article id {article_id}")

    for duplicate in sorted({item for item in configured_ids if configured_ids.count(item) > 1}):
        errors.append(f"duplicate configured article id: {duplicate}")
    for duplicate in sorted({item for item in all_ids if all_ids.count(item) > 1}):
        errors.append(f"duplicate HTML id across components: {duplicate}")
    for target in sorted(set(all_links) - set(all_ids)):
        errors.append(f"section link has no target: #{target}")
    for article_id in configured_ids:
        if parsed_article_ids.count(article_id) != 1:
            errors.append(f"article id must occur once in components: {article_id}")

    index_source = (root / "index.html").read_text(encoding="utf-8") if (root / "index.html").is_file() else ""
    for required_reference in ("data/report-config.json", "scripts/main.js", "styles/base.css"):
        if required_reference not in index_source:
            errors.append(f"index.html does not reference {required_reference}")

    if errors:
        fail(errors)

    print(f"Report validation passed: {root}")
    print(f"Articles: {len(articles)} | Unique ids: {len(all_ids)} | Section links: {len(all_links)}")


if __name__ == "__main__":
    main()

