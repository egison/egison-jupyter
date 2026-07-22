"""Validate coverage, structure, metadata, and stored Egison outputs."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import nbformat

from tools.math_notebooks.catalog import CATALOG, EXPECTED_SLUGS
from tools.math_notebooks.common import KERNEL_METADATA, NOTEBOOK_DIR, REPOSITORY_ROOT


BAD_OUTPUT = re.compile(
    r"Type error:|Evaluation error:|Parse error:|Warning:|"
    r"Unbound variable|Restarting Egison|Traceback \(most recent call last\)"
)


def output_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from output_strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from output_strings(item)


def validate_notebook(path: Path, require_outputs: bool) -> list[str]:
    problems: list[str] = []
    notebook = nbformat.read(path, as_version=4)

    try:
        nbformat.validate(notebook)
    except Exception as error:  # pragma: no cover - diagnostic path
        problems.append(f"invalid nbformat: {error}")

    if notebook.metadata != KERNEL_METADATA:
        problems.append("kernel/language metadata differs from the canonical metadata")
    if (notebook.nbformat, notebook.nbformat_minor) != (4, 5):
        problems.append("notebook format must be 4.5")

    markdown_cells = [cell for cell in notebook.cells if cell.cell_type == "markdown"]
    code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    if len(markdown_cells) < 4:
        problems.append("fewer than four explanatory Markdown cells")
    if len(code_cells) < 3:
        problems.append("fewer than three Egison code cells")
    if not notebook.cells or notebook.cells[0].cell_type != "markdown":
        problems.append("first cell is not Markdown")
    elif not notebook.cells[0].source.lstrip().startswith("# "):
        problems.append("first cell does not start with an H1 title")

    ids = [cell.id for cell in notebook.cells]
    if len(ids) != len(set(ids)):
        problems.append("duplicate cell ids")

    for index, cell in enumerate(notebook.cells):
        if not cell.source.strip():
            problems.append(f"cell {index} is empty")
        if cell.cell_type == "code":
            if "assertEqual" in cell.source or "(define $" in cell.source:
                problems.append(f"cell {index} contains test or legacy syntax")
            if cell.metadata:
                problems.append(f"cell {index} contains transient metadata")
            for text in output_strings(cell.get("outputs", [])):
                if BAD_OUTPUT.search(text):
                    problems.append(f"cell {index} contains an Egison/Jupyter error: {text[:100]!r}")

    if require_outputs:
        executed = [cell for cell in code_cells if cell.execution_count is not None]
        rich_outputs = [
            output
            for cell in code_cells
            for output in cell.outputs
            if output.output_type == "display_data" and "text/html" in output.get("data", {})
        ]
        if len(executed) != len(code_cells):
            problems.append("not every code cell has been executed")
        if len(rich_outputs) < 2:
            problems.append("fewer than two stored LaTeX display outputs")

    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-outputs", action="store_true")
    parser.add_argument(
        "--notebook-dir",
        type=Path,
        default=NOTEBOOK_DIR,
        help="directory containing the mathematics notebooks",
    )
    args = parser.parse_args()

    notebook_directory = args.notebook_dir.resolve()
    actual = {path.stem for path in notebook_directory.glob("*.ipynb")}
    problems: list[str] = []
    missing = sorted(EXPECTED_SLUGS - actual)
    unexpected = sorted(actual - EXPECTED_SLUGS)
    if missing:
        problems.append(f"missing notebooks: {', '.join(missing)}")
    if unexpected:
        problems.append(f"unexpected notebooks: {', '.join(unexpected)}")

    for _, slug, _ in CATALOG:
        path = notebook_directory / f"{slug}.ipynb"
        if path.exists():
            for problem in validate_notebook(path, args.require_outputs):
                problems.append(f"{path.name}: {problem}")

    if problems:
        print("\n".join(problems))
        return 1
    try:
        display_directory = notebook_directory.relative_to(REPOSITORY_ROOT)
    except ValueError:
        display_directory = notebook_directory
    print(
        f"Validated {len(CATALOG)} mathematics notebooks in "
        f"{display_directory}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
