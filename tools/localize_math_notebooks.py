#!/usr/bin/env python3
"""Build Japanese notebooks from canonical executed notebooks and translations."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
from collections import Counter
from pathlib import Path

import nbformat


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRECTORY = REPOSITORY_ROOT / "math"
TRANSLATION_DIRECTORY = REPOSITORY_ROOT / "translations" / "ja" / "math"
OUTPUT_DIRECTORY = REPOSITORY_ROOT / "ja" / "math"
HEADER = re.compile(
    r"\A<!--\n"
    r"notebook: (?P<slug>[A-Za-z0-9-]+)\n"
    r"source-markdown-sha256: (?P<digest>[0-9a-f]{64})\n"
    r"-->\n"
)
CELL_MARKER = re.compile(r"^<!-- cell: (?P<cell_id>[0-9a-f]{8}) -->\n", re.MULTILINE)
JAPANESE_TEXT = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
STRUCTURAL_TOKENS = {
    "display math": re.compile(r"\$\$.*?\$\$", re.DOTALL),
    "inline math": re.compile(
        r"(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)", re.DOTALL
    ),
    "inline code": re.compile(r"`[^`]+`"),
    "URL": re.compile(r"https?://[^\s)>]+"),
}
HEADING = re.compile(r"^(?P<marks>#+)\s", re.MULTILINE)


def markdown_cells(notebook: dict) -> list[dict]:
    return [cell for cell in notebook["cells"] if cell["cell_type"] == "markdown"]


def markdown_digest(notebook: dict) -> str:
    digest = hashlib.sha256()
    for cell in markdown_cells(notebook):
        digest.update(cell["id"].encode())
        digest.update(b"\0")
        source = cell["source"]
        if isinstance(source, list):
            source = "".join(source)
        digest.update(source.encode())
        digest.update(b"\0")
    return digest.hexdigest()


def source_text(cell: dict) -> str:
    source = cell["source"]
    return "".join(source) if isinstance(source, list) else source


def translation_template(slug: str, notebook: dict) -> str:
    sections = [
        "<!--",
        f"notebook: {slug}",
        f"source-markdown-sha256: {markdown_digest(notebook)}",
        "-->",
        "",
    ]
    for cell in markdown_cells(notebook):
        sections.append(f"<!-- cell: {cell['id']} -->")
        sections.append(source_text(cell).strip("\n"))
        sections.append("")
    return "\n".join(sections).rstrip() + "\n"


def parse_translation(path: Path, slug: str, notebook: dict) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    header = HEADER.match(text)
    if not header:
        raise ValueError(f"{path.name}: invalid translation header")
    if header.group("slug") != slug:
        raise ValueError(f"{path.name}: notebook slug does not match {slug}")

    expected_digest = markdown_digest(notebook)
    if header.group("digest") != expected_digest:
        raise ValueError(
            f"{path.name}: English Markdown changed; refresh and review the translation"
        )

    markers = list(CELL_MARKER.finditer(text, header.end()))
    translations: dict[str, str] = {}
    for index, marker in enumerate(markers):
        start = marker.end()
        end = markers[index + 1].start() if index + 1 < len(markers) else len(text)
        cell_id = marker.group("cell_id")
        if cell_id in translations:
            raise ValueError(f"{path.name}: duplicate translation for cell {cell_id}")
        translation = text[start:end].strip("\n") + "\n"
        if not translation.strip():
            raise ValueError(f"{path.name}: empty translation for cell {cell_id}")
        if not JAPANESE_TEXT.search(translation):
            raise ValueError(f"{path.name}: cell {cell_id} contains no Japanese text")
        translations[cell_id] = translation

    expected_ids = {cell["id"] for cell in markdown_cells(notebook)}
    actual_ids = set(translations)
    if actual_ids != expected_ids:
        missing = sorted(expected_ids - actual_ids)
        unexpected = sorted(actual_ids - expected_ids)
        details = []
        if missing:
            details.append(f"missing cells: {', '.join(missing)}")
        if unexpected:
            details.append(f"unexpected cells: {', '.join(unexpected)}")
        raise ValueError(f"{path.name}: {'; '.join(details)}")

    for cell in markdown_cells(notebook):
        original = source_text(cell)
        translation = translations[cell["id"]]
        for label, pattern in STRUCTURAL_TOKENS.items():
            if Counter(pattern.findall(original)) != Counter(
                pattern.findall(translation)
            ):
                raise ValueError(
                    f"{path.name}: cell {cell['id']} changed a {label} token"
                )
        original_headings = [
            len(match.group("marks")) for match in HEADING.finditer(original)
        ]
        translated_headings = [
            len(match.group("marks")) for match in HEADING.finditer(translation)
        ]
        if original_headings != translated_headings:
            raise ValueError(
                f"{path.name}: cell {cell['id']} changed Markdown heading levels"
            )
    return translations


def localized_notebook(path: Path, translations: dict[str, str]) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    original_code = [
        json.dumps(cell, ensure_ascii=False, sort_keys=True)
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
    ]

    for cell in notebook["cells"]:
        if cell["cell_type"] == "markdown":
            cell["source"] = translations[cell["id"]].splitlines(keepends=True)

    localized_code = [
        json.dumps(cell, ensure_ascii=False, sort_keys=True)
        for cell in notebook["cells"]
        if cell["cell_type"] == "code"
    ]
    if localized_code != original_code:
        raise ValueError(f"{path.name}: localization changed a code cell or its outputs")

    nbformat.validate(nbformat.from_dict(notebook))
    return json.dumps(notebook, ensure_ascii=False, indent=1) + "\n"


def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as temporary:
        temporary.write(content)
        temporary_path = Path(temporary.name)
    temporary_path.chmod(0o644)
    temporary_path.replace(path)


def initialize_translations(notebooks: dict[str, Path]) -> int:
    TRANSLATION_DIRECTORY.mkdir(parents=True, exist_ok=True)
    created = 0
    for slug, path in sorted(notebooks.items()):
        destination = TRANSLATION_DIRECTORY / f"{slug}.md"
        if destination.exists():
            continue
        notebook = json.loads(path.read_text(encoding="utf-8"))
        write_atomic(destination, translation_template(slug, notebook))
        created += 1
    print(f"Initialized {created} Japanese translation files.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--initialize",
        action="store_true",
        help="create missing translation files with English Markdown as placeholders",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify that all Japanese notebooks are current without writing",
    )
    args = parser.parse_args()

    notebooks = {path.stem: path for path in SOURCE_DIRECTORY.glob("*.ipynb")}
    if args.initialize:
        return initialize_translations(notebooks)

    translation_paths = {
        path.stem: path for path in TRANSLATION_DIRECTORY.glob("*.md")
    }
    if set(translation_paths) != set(notebooks):
        missing = sorted(set(notebooks) - set(translation_paths))
        unexpected = sorted(set(translation_paths) - set(notebooks))
        details = []
        if missing:
            details.append(f"missing translations: {', '.join(missing)}")
        if unexpected:
            details.append(f"unexpected translations: {', '.join(unexpected)}")
        raise SystemExit("; ".join(details))

    stale: list[Path] = []
    changed = 0
    for slug, source_path in sorted(notebooks.items()):
        notebook = json.loads(source_path.read_text(encoding="utf-8"))
        translations = parse_translation(
            translation_paths[slug], slug, notebook
        )
        rendered = localized_notebook(source_path, translations)
        destination = OUTPUT_DIRECTORY / f"{slug}.ipynb"
        current = destination.read_text(encoding="utf-8") if destination.exists() else None
        if current == rendered:
            continue
        if args.check:
            stale.append(destination)
        else:
            write_atomic(destination, rendered)
            changed += 1

    if stale:
        for path in stale:
            print(f"out of date: {path.relative_to(REPOSITORY_ROOT)}")
        return 1

    action = "Verified" if args.check else "Localized"
    detail = "" if args.check else f" ({changed} changed)"
    print(f"{action} {len(notebooks)} Japanese mathematics notebooks{detail}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
