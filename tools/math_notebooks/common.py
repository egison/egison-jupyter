"""Shared helpers for building deterministic Egison notebooks."""

from __future__ import annotations

import hashlib
import json
import textwrap
from pathlib import Path
from typing import Iterable


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK_DIR = REPOSITORY_ROOT / "math"

KERNEL_METADATA = {
    "kernelspec": {
        "display_name": "Egison",
        "language": "egison",
        "name": "egison",
    },
    "language_info": {
        "codemirror_mode": "egison",
        "file_extension": ".egi",
        "mimetype": "text/x-egison",
        "name": "egison",
    },
}


def _source(text: str) -> list[str]:
    normalized = textwrap.dedent(text).strip("\n") + "\n"
    return normalized.splitlines(keepends=True)


def markdown(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": _source(text),
    }


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": _source(text),
    }


def write_notebook(slug: str, cells: Iterable[dict]) -> Path:
    notebook_cells = list(cells)
    if not notebook_cells or notebook_cells[0]["cell_type"] != "markdown":
        raise ValueError(f"{slug}: the first cell must be Markdown")

    for index, cell in enumerate(notebook_cells):
        digest = hashlib.sha1(f"{slug}:{index}".encode()).hexdigest()[:8]
        cell["id"] = digest

    notebook = {
        "cells": notebook_cells,
        "metadata": KERNEL_METADATA,
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    destination = NOTEBOOK_DIR / f"{slug}.ipynb"
    destination.write_text(
        json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8",
    )
    return destination
