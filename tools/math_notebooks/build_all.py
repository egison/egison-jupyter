"""Regenerate all route-mapped mathematics notebooks."""

from . import algebra_number, analysis, emr, forms_physics, riemann
from .catalog import EXPECTED_SLUGS
from .common import NOTEBOOK_DIR


def main() -> None:
    algebra_number.main()
    analysis.build()
    riemann.build()
    emr.build()
    forms_physics.main()

    actual = {path.stem for path in NOTEBOOK_DIR.glob("*.ipynb")}
    if actual != EXPECTED_SLUGS:
        missing = sorted(EXPECTED_SLUGS - actual)
        unexpected = sorted(actual - EXPECTED_SLUGS)
        raise RuntimeError(f"coverage mismatch: missing={missing}, unexpected={unexpected}")
    print(f"Generated {len(actual)} mathematics notebooks in {NOTEBOOK_DIR}")


if __name__ == "__main__":
    main()
