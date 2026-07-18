"""Remove transient per-cell metadata without changing saved notebook outputs."""

from __future__ import annotations

from pathlib import Path

import nbformat

from tools.math_notebooks.common import NOTEBOOK_DIR


def normalize_notebook(path: Path) -> int:
    notebook = nbformat.read(path, as_version=4)
    changed = 0

    for cell in notebook.cells:
        if cell.metadata:
            cell.metadata = {}
            changed += 1

    if changed:
        nbformat.write(notebook, path)
    return changed


def main() -> int:
    notebooks = sorted(NOTEBOOK_DIR.glob("*.ipynb"))
    changed_cells = sum(normalize_notebook(path) for path in notebooks)
    print(
        f"Normalized {len(notebooks)} mathematics notebooks "
        f"({changed_cells} cells changed)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
