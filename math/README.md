# Egison Mathematics Notebooks

These 43 self-contained notebooks correspond one-to-one with the routable demo
pages under `www.egison.org/math`.  Each notebook uses the page basename as its
slug, so `www.egison.org/math/<slug>.html` maps directly to `<slug>.ipynb`.

The notebooks use the Egison 5 kernel, current `def` syntax, typed symbolic
definitions, explanatory English Markdown, and LaTeX mathematics.  Run each
notebook from a fresh kernel, from top to bottom.

## Number Theory

- [Tribonacci Number](tribonacci.ipynb)
- [Euler's Totient Function](eulers-totient-function.ipynb)
- [Gaussian Primes](gaussian-primes.ipynb)
- [Eisenstein Primes](eisenstein-primes.ipynb)

## Algebra

- [Quadratic Equation](quadratic-equation.ipynb)
- [Cubic Equation](cubic-equation.ipynb)
- [Quartic Equation](quartic-equation.ipynb)
- [5th Roots of Unity](5th-root-of-unity.ipynb)
- [7th Roots of Unity](7th-root-of-unity.ipynb)
- [9th Roots of Unity](9th-root-of-unity.ipynb)
- [17th Roots of Unity](17th-root-of-unity.ipynb)

## Mathematical Analysis

- [The Order of Partial Differentiation](order-of-partial-derivative.ipynb)
- [Laplacian in Polar Coordinates](polar-laplacian-2d.ipynb)
- [Laplacian in Spherical Coordinates](polar-laplacian-3d.ipynb)
- [Laplacian, Hessian, and Jacobian](laplacian-hessian-jacobian.ipynb)
- [Euler's Formula](eulers-formula.ipynb)
- [Fourier Series](fourier-series.ipynb)
- [Leibniz Formula](leibniz-formula.ipynb)

## Geometry and Physics

- [Trigonometric Identities](trigonometric-identities.ipynb)
- [Gaussian Curvature of a Surface](gaussian-curvature-of-surface.ipynb)
- [Riemann Curvature Tensor of S²](riemann-curvature-tensor-of-S2.ipynb)
- [Riemann Curvature Tensor of S³](riemann-curvature-tensor-of-S3.ipynb)
- [Riemann Curvature Tensor of S⁴](riemann-curvature-tensor-of-S4.ipynb)
- [Riemann Curvature Tensor of S⁵](riemann-curvature-tensor-of-S5.ipynb)
- [Riemann Curvature Tensor of S⁷](riemann-curvature-tensor-of-S7.ipynb)
- [Riemann Curvature Tensor of T²](riemann-curvature-tensor-of-T2.ipynb)
- [An Einstein Metric on S² × S³](riemann-curvature-tensor-of-S2xS3.ipynb)
- [Schwarzschild Metric](riemann-curvature-tensor-of-Schwarzschild-metric.ipynb)
- [FLRW Metric](riemann-curvature-tensor-of-FLRW-metric.ipynb)
- [Wedge Product](wedge-product.ipynb)
- [Exterior Derivative](exterior-derivative.ipynb)
- [Hodge Star in E³](hodge-E3.ipynb)
- [Hodge Star in Minkowski Spacetime](hodge-minkowski.ipynb)
- [Hodge Laplacian in Polar Coordinates](hodge-laplacian-polar.ipynb)
- [Hodge Laplacian in Spherical Coordinates](hodge-laplacian-spherical.ipynb)
- [Curvature Form](curvature-form.ipynb)
- [Vector Analysis](vector-analysis.ipynb)
- [U(1) Yang–Mills Theory](yang-mills-equation-of-U1-gauge-theory.ipynb)
- [Euler Form of S²](euler-form-of-S2.ipynb)
- [Euler Form of T²](euler-form-of-T2.ipynb)
- [First Chern Form on CP¹](chern-form-of-CP1.ipynb)
- [Highest-Power Coefficient in the EMR Curvature Formula](emr-highest-power-coefficient.ipynb)
- [Wodzicki–Chern–Simons Invariant on the Thurston Example](emr-thurston-wcs-invariant.ipynb)

## Maintenance

The topic builders under `tools/math_notebooks/` generate deterministic cell
IDs and canonical kernel metadata.  Regenerating a notebook clears its stored
outputs, so execute it again before publishing.

Regenerate all source notebooks with:

```sh
python3 -m tools.math_notebooks.build_all
```

Validate coverage and structure with:

```sh
.venv/bin/python -m tools.validate_math_notebooks
```

After executing all notebooks, also require stored outputs:

```sh
.venv/bin/python -m tools.normalize_math_notebooks
.venv/bin/python -m tools.validate_math_notebooks --require-outputs
```

The normalization step removes transient per-cell timing metadata while
preserving execution counts and rendered outputs.
