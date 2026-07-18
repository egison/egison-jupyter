"""Build the surface-geometry and Riemann-curvature demo notebooks.

The notebooks in this module are deliberately source-oriented: definition cells
set up a reusable tensor calculation, while the following small query cells are
good places for Jupyter to store representative results.  Large space-time and
Einstein-metric examples define the complete contraction pipeline but avoid a
full symbolic expansion as an automatic output cell.
"""

from __future__ import annotations

from pathlib import Path

from .common import code, markdown, write_notebook


SPHERES: tuple[tuple[int, str, tuple[str, ...]], ...] = (
    (2, "S2", ("θ", "φ")),
    (3, "S3", ("θ", "φ", "ψ")),
    (4, "S4", ("θ", "φ", "ψ", "η")),
    (5, "S5", ("θ", "φ", "ψ", "η", "δ")),
    (7, "S7", ("α", "β", "γ", "δ", "ξ", "ζ", "η")),
)

LATEX_NAMES = {
    "θ": r"\theta",
    "φ": r"\phi",
    "ψ": r"\psi",
    "η": r"\eta",
    "δ": r"\delta",
    "α": r"\alpha",
    "β": r"\beta",
    "γ": r"\gamma",
    "ξ": r"\xi",
    "ζ": r"\zeta",
}


def _vector(entries: list[str]) -> str:
    return "[| " + ", ".join(entries) + " |]"


def _diagonal_matrix(entries: list[str], suffix: str) -> str:
    rows: list[str] = []
    for row, entry in enumerate(entries):
        cells = ["0"] * len(entries)
        cells[row] = entry
        rows.append("[| " + ", ".join(cells) + " |]")
    return "[| " + "\n              , ".join(rows) + f"\n              |]{suffix}"


def _sphere_embedding(angles: tuple[str, ...]) -> list[str]:
    entries: list[str] = []
    sine_prefix: list[str] = []
    for angle in angles:
        factors = ["r", *sine_prefix, f"cos {angle}"]
        entries.append(" * ".join(factors))
        sine_prefix.append(f"sin {angle}")
    entries.append(" * ".join(["r", *sine_prefix]))
    return entries


def _sphere_metric_entries(angles: tuple[str, ...]) -> tuple[list[str], list[str]]:
    covariant: list[str] = []
    contravariant: list[str] = []
    preceding: list[str] = []
    for _angle in angles:
        covariant.append(" * ".join(["r^2", *[f"(sin {a})^2" for a in preceding]]))
        contravariant.append(
            " * ".join(["r^(-2)", *[f"(sin {a})^(-2)" for a in preceding]])
        )
        preceding.append(_angle)
    return covariant, contravariant


def _sphere_line_element(angles: tuple[str, ...]) -> str:
    terms: list[str] = []
    preceding: list[str] = []
    for angle in angles:
        coefficient = " ".join(rf"\sin^2 {LATEX_NAMES[a]}" for a in preceding)
        differential = rf"d{LATEX_NAMES[angle]}^2"
        terms.append(f"{coefficient} {differential}".strip())
        preceding.append(angle)
    return " + ".join(terms)


def _sphere_cells(dimension: int, angles: tuple[str, ...]) -> list[dict]:
    coordinate_text = ", ".join(LATEX_NAMES[a] for a in angles)
    first = LATEX_NAMES[angles[0]]
    second = LATEX_NAMES[angles[1]]
    covariant, contravariant = _sphere_metric_entries(angles)
    embedding = _sphere_embedding(angles)

    cells = [
        markdown(
            rf"""
            # Riemann Curvature Tensor of $S^{dimension}$

            A round {dimension}-sphere of radius $r$ has constant sectional curvature
            $1/r^2$.  This notebook builds its metric, Levi-Civita connection, Riemann
            tensor, Ricci tensor, and scalar curvature in indexed Egison notation.

            We use the convention

            $$
            R^i{{}}_{{jkl}}
              = \partial_k\Gamma^i{{}}_{{jl}}
              - \partial_l\Gamma^i{{}}_{{jk}}
              + \Gamma^m{{}}_{{jl}}\Gamma^i{{}}_{{mk}}
              - \Gamma^m{{}}_{{jk}}\Gamma^i{{}}_{{ml}}.
            $$
            """
        ),
        markdown(
            rf"""
            ## Hyperspherical chart

            The coordinates are $x=({coordinate_text})$.  The standard embedding
            $X:S^{dimension}\hookrightarrow\mathbb{{R}}^{dimension + 1}$ is built by
            successively multiplying by sines: $X_1=r\cos {first}$,
            $X_2=r\sin {first}\cos {second}$, and so on.  It makes
            $X\mathbin{{\cdot}}X=r^2$ manifest.

            The chart excludes the usual coordinate poles; those singularities are
            features of hyperspherical coordinates, not of the round geometry.
            """
        ),
        code(
            f"""
            declare symbol r, {', '.join(angles)}: MathValue

            def x : Vector MathValue := {_vector(list(angles))}

            def X : Vector MathValue := {_vector(embedding)}
            """
        ),
        code("X"),
        markdown(
            rf"""
            ## Metric and inverse metric

            Differentiating the embedding gives an orthogonal coordinate basis.  Its
            line element is

            $$
            ds^2=r^2\left({_sphere_line_element(angles)}\right).
            $$

            We enter this diagonal result explicitly.  That keeps the notebook quick
            while retaining the same metric derived from
            $g_{{ij}}=\partial_iX\mathbin{{\cdot}}\partial_jX$.
            """
        ),
        code(
            f"""
            def g_i_j : Matrix MathValue :=
              {_diagonal_matrix(covariant, '_i_j')}

            def g~i~j : Matrix MathValue :=
              {_diagonal_matrix(contravariant, '~i~j')}
            """
        ),
    ]

    if dimension <= 3:
        cells.extend([code("g_#_#"), code("g~#~#")])
    else:
        cells.extend([code("g_1_#"), code(f"g_{dimension}_#"), code("g~1~#")])

    cells.extend(
        [
            markdown(
                r"""
                ## Levi-Civita connection

                The Christoffel symbols of the first kind and second kind are

                $$
                \Gamma_{ijk}=\frac12
                (\partial_jg_{ik}+\partial_kg_{ij}-\partial_ig_{jk}),
                \qquad
                \Gamma^i{}_{jk}=g^{im}\Gamma_{mjk}.
                $$

                Repeated symbolic indices are contracted by `.`.  The `withSymbols`
                block makes the dummy index local to the definition.
                """
            ),
            code(
                """
                def Γ_i_j_k : Tensor MathValue :=
                  (1 / 2) * (∂/∂ g_i_k x~j + ∂/∂ g_i_j x~k - ∂/∂ g_j_k x~i)

                def Γ~i_j_k : Tensor MathValue := withSymbols [m]
                  g~i~m . Γ_m_j_k
                """
            ),
        ]
    )

    if dimension == 2:
        cells.extend([code("Γ~1_#_#"), code("Γ~2_#_#")])
    else:
        cells.extend([code("Γ~1_2_2"), code("Γ~2_1_2")])

    cells.extend(
        [
            markdown(
                r"""
                ## Riemann tensor

                The following definition is a direct transcription of the stated
                convention.  The two output cells sample the same coordinate
                two-plane with the first two tensor slots exchanged; their different
                coordinate factors are exactly what one expects in a non-orthonormal
                coordinate basis.
                """
            ),
            code(
                """
                def R~i_j_k_l : Tensor MathValue := withSymbols [m]
                  ∂/∂ Γ~i_j_l x~k - ∂/∂ Γ~i_j_k x~l
                    + Γ~m_j_l . Γ~i_m_k - Γ~m_j_k . Γ~i_m_l
                """
            ),
        ]
    )

    if dimension == 2:
        cells.extend([code("R~#_#_1_2"), code("R~#_#_2_1")])
    else:
        cells.extend([code("R~1_2_1_2"), code("R~2_1_1_2")])

    cells.extend(
        [
            markdown(
                rf"""
                ## Ricci and scalar curvature

                Contracting the first and third Riemann indices gives

                $$
                \operatorname{{Ric}}_{{ij}}=R^m{{}}_{{imj}},
                \qquad
                \mathcal{{R}}=g^{{ij}}\operatorname{{Ric}}_{{ij}}.
                $$

                For a round $S^{dimension}$ the coordinate-free prediction is

                $$
                \operatorname{{Ric}}=\frac{{{dimension - 1}}}{{r^2}}g,
                \qquad
                \mathcal{{R}}=\frac{{{dimension * (dimension - 1)}}}{{r^2}}.
                $$
                """
            ),
            code(
                """
                def Ric_i_j : Matrix MathValue := withSymbols [m]
                  sum (contract R~m_i_m_j)

                def scalarCurvature : MathValue := withSymbols [i, j]
                  g~i~j . Ric_i_j
                """
            ),
        ]
    )

    if dimension == 2:
        cells.extend([code("Ric_#_#"), code("scalarCurvature")])
    elif dimension == 3:
        cells.extend([code("Ric_#_#"), code("scalarCurvature")])
    elif dimension <= 4:
        cells.extend([code("Ric_1_#"), code("scalarCurvature")])

    high_dimension_note = ""
    if dimension >= 5:
        high_dimension_note = (
            "  The Ricci and scalar-curvature definitions are present, but their full "
            "contractions are intentionally not output cells: the selected Riemann "
            "components demonstrate the constant-curvature pattern without forcing "
            "a large symbolic expansion."
        )

    cells.append(
        markdown(
            rf"""
            ## Interpretation

            The sampled components are coordinate dependent, but their contractions
            recover the invariant statement: every tangent two-plane has sectional
            curvature $1/r^2$, the metric is Einstein, and the scalar curvature is
            ${dimension * (dimension - 1)}/r^2$.  Factors such as $\sin {first}$ vanish
            at chart poles because the coordinate frame degenerates there; the
            curvature itself remains smooth.{high_dimension_note}
            """
        )
    )
    return cells


def _surface_cells() -> list[dict]:
    return [
        markdown(
            r"""
            # Gaussian and Mean Curvature of a Graph Surface

            Let a surface in Euclidean three-space be the graph

            $$
            X(x,y)=(x,y,f(x,y)).
            $$

            This notebook derives both fundamental forms and then computes the
            Gaussian curvature $K$ and mean curvature $H$.  Egison keeps the
            derivatives of the arbitrary function $f$ symbolic.
            """
        ),
        markdown(
            r"""
            ## Tangent plane

            The coordinate tangent vectors are

            $$
            X_x=(1,0,f_x),\qquad X_y=(0,1,f_y).
            $$

            Their cross product is $(-f_x,-f_y,1)$, so its norm is
            $W=\sqrt{1+f_x^2+f_y^2}$.
            """
        ),
        code(
            """
            declare symbol x, y: MathValue

            def f : MathValue := function (x, y)
            def X : Vector MathValue := [| x, y, f x y |]

            def vx : Vector MathValue := [| 1, 0, ∂/∂ (f x y) x |]
            def vy : Vector MathValue := [| 0, 1, ∂/∂ (f x y) y |]
            """
        ),
        code("vx"),
        code("vy"),
        markdown(
            r"""
            ## Oriented unit normal

            We choose the upward-pointing normal

            $$
            n=\frac{X_x\times X_y}{\lVert X_x\times X_y\rVert}.
            $$

            Reversing this orientation changes the sign of $H$ but not of $K$.
            """
        ),
        code(
            """
            def normalNumerator : Vector MathValue := crossProduct vx vy
            def W : MathValue := sqrt (V.* normalNumerator normalNumerator)
            def normal : Vector MathValue := normalNumerator / W
            """
        ),
        code("normalNumerator"),
        code("normal"),
        markdown(
            r"""
            ## First and second fundamental forms

            With

            $$
            I=E\,dx^2+2F\,dx\,dy+G\,dy^2,
            \qquad
            II=L\,dx^2+2M\,dx\,dy+N\,dy^2,
            $$

            the coefficients are dot products of tangent vectors and derivatives of
            tangent vectors with the chosen normal.
            """
        ),
        code(
            """
            def E : MathValue := V.* vx vx
            def F : MathValue := V.* vx vy
            def G : MathValue := V.* vy vy

            def L : MathValue := V.* (∂/∂ vx x) normal
            def M : MathValue := V.* (∂/∂ vx y) normal
            def N : MathValue := V.* (∂/∂ vy y) normal
            """
        ),
        code("(E, F, G)"),
        code("(L, M, N)"),
        markdown(
            r"""
            ## Curvature

            The determinant and trace of the shape operator give

            $$
            K=\frac{LN-M^2}{EG-F^2},\qquad
            H=\frac{EN-2FM+GL}{2(EG-F^2)}.
            $$

            These formulas apply wherever the graph chart is regular.  For a graph,
            $EG-F^2=1+f_x^2+f_y^2$ is always positive.
            """
        ),
        code(
            """
            def K : MathValue := (L * N - M^2) / (E * G - F^2)
            def H : MathValue := (E * N - 2 * F * M + G * L) / (2 * (E * G - F^2))
            """
        ),
        code("K"),
        code("H"),
        markdown(
            r"""
            ## Interpretation

            $K$ is intrinsic: it can be recovered entirely from distances measured on
            the surface.  Positive, zero, and negative values correspond locally to
            elliptic, parabolic, and hyperbolic behavior.  $H$ is extrinsic and depends
            on the embedding and orientation; the equation $H=0$ is the minimal-surface
            equation for a graph.
            """
        ),
    ]


def _torus_cells() -> list[dict]:
    return [
        markdown(
            r"""
            # Riemann Curvature Tensor of the Embedded Torus $T^2$

            A ring torus with tube radius $a$ and major radius $b$ is embedded by

            $$
            X(\theta,\phi)=\bigl((b+a\cos\theta)\cos\phi,
            (b+a\cos\theta)\sin\phi,a\sin\theta\bigr),\qquad b>a>0.
            $$

            Unlike the intrinsically flat quotient torus, this embedded torus has
            curvature that changes sign.  We compute its connection, Riemann tensor,
            Ricci tensor, and scalar curvature.
            """
        ),
        markdown(
            r"""
            ## Coordinates and metric

            The coordinate vectors are orthogonal and have squared lengths $a^2$ and
            $(b+a\cos\theta)^2$.  Therefore

            $$
            g=\begin{pmatrix}a^2&0\\0&(b+a\cos\theta)^2\end{pmatrix}.
            $$
            """
        ),
        code(
            """
            declare symbol a, b, θ, φ: MathValue

            def x : Vector MathValue := [| θ, φ |]
            def X : Vector MathValue :=
              [| `(a * cos θ + b) * cos φ
               , `(a * cos θ + b) * sin φ
               , a * sin θ
               |]

            def g_i_j : Matrix MathValue :=
              [| [| a^2, 0 |], [| 0, `(a * cos θ + b)^2 |] |]_i_j

            def g~i~j : Matrix MathValue :=
              [| [| a^(-2), 0 |], [| 0, `(a * cos θ + b)^(-2) |] |]~i~j
            """
        ),
        code("X"),
        code("g_#_#"),
        code("g~#~#"),
        markdown(
            r"""
            ## Levi-Civita connection

            We use
            $\Gamma_{ijk}=\tfrac12(\partial_jg_{ik}+\partial_kg_{ij}-\partial_ig_{jk})$
            and raise the first index with $g^{ij}$.
            """
        ),
        code(
            """
            def Γ_i_j_k : Tensor MathValue :=
              (1 / 2) * (∂/∂ g_i_k x~j + ∂/∂ g_i_j x~k - ∂/∂ g_j_k x~i)

            def Γ~i_j_k : Tensor MathValue := withSymbols [m]
              g~i~m . Γ_m_j_k
            """
        ),
        code("Γ~1_#_#"),
        code("Γ~2_#_#"),
        markdown(
            r"""
            ## Riemann tensor

            The last two indices are antisymmetric.  Lowering the first index also
            exposes the familiar pair symmetries of $R_{ijkl}$.
            """
        ),
        code(
            """
            def R~i_j_k_l : Tensor MathValue := withSymbols [m]
              ∂/∂ Γ~i_j_l x~k - ∂/∂ Γ~i_j_k x~l
                + Γ~m_j_l . Γ~i_m_k - Γ~m_j_k . Γ~i_m_l

            def R_i_j_k_l : Tensor MathValue := withSymbols [m]
              g_i_m . R~m_j_k_l
            """
        ),
        code("R~#_#_1_2"),
        code("R_1_2_1_2"),
        markdown(
            r"""
            ## Ricci, scalar, and Gaussian curvature

            In two dimensions the scalar curvature is twice the Gaussian curvature:
            $\mathcal R=2K$.  For this torus,

            $$
            K(\theta)=\frac{\cos\theta}{a(b+a\cos\theta)}.
            $$
            """
        ),
        code(
            """
            def Ric_i_j : Matrix MathValue := withSymbols [m]
              sum (contract R~m_i_m_j)

            def scalarCurvature : MathValue := withSymbols [i, j]
              g~i~j . Ric_i_j

            def gaussianCurvature : MathValue := scalarCurvature / 2
            """
        ),
        code("Ric_#_#"),
        code("scalarCurvature"),
        code("gaussianCurvature"),
        markdown(
            r"""
            ## Interpretation

            The outside of the torus ($\cos\theta>0$) is positively curved, the inside
            ($\cos\theta<0$) is negatively curved, and the top and bottom circles are
            parabolic.  The positive and negative contributions cancel in the
            Gauss--Bonnet integral, consistently with $\chi(T^2)=0$.
            """
        ),
    ]


def _s2xs3_cells() -> list[dict]:
    return [
        markdown(
            r"""
            # An Einstein Metric on $S^2\times S^3$

            The historical Egison demo bearing the name “Riemann curvature tensor of
            $S^2\times S^3$” uses a non-diagonal five-dimensional metric, not the
            elementary block product of two round metrics.  Its goal is the Einstein
            identity

            $$
            \operatorname{Ric}_{ij}=4g_{ij},\qquad \mathcal R=20.
            $$

            This notebook preserves that metric and makes its symbolic workload
            explicit.  Small metric and connection components are suitable interactive
            outputs; the full Einstein residual is defined for deliberate evaluation.
            """
        ),
        markdown(
            r"""
            ## Coordinates and abbreviations

            In the coordinate order $x=(\phi,\theta,\psi,y,\alpha)$, introduce

            $$
            p=1-y,\quad u=a-y^2,\quad
            v=a-3y^2+2y^3,\quad q=a-2y+y^2.
            $$

            These factors expose the repeated structure of the source metric and make
            its coordinate domain restrictions ($p u v\ne0$) visible.
            """
        ),
        code(
            """
            declare symbol φ, θ, ψ, y, α, a: MathValue

            def x : Vector MathValue := [| φ, θ, ψ, y, α |]

            def p : MathValue := `(1 - y)
            def u : MathValue := `(a - y^2)
            def v : MathValue := `(a - 3 * y^2 + 2 * y^3)
            def q : MathValue := `(a - 2 * y + y^2)
            """
        ),
        code("(p, u, v, q)"),
        markdown(
            r"""
            ## Metric

            The nonzero entries, together with their symmetric partners, are

            $$
            \begin{aligned}
            g_{11}&=\frac{3p^2u\sin^2\theta+2vp\cos^2\theta+q^2\cos^2\theta}{18up},
            &g_{13}&=\frac{-2vp\cos\theta-q^2\cos\theta}{18up},\\
            g_{15}&=-\frac{q\cos\theta}{3p},
            &g_{22}&=\frac p6,\\
            g_{33}&=\frac{2vp+q^2}{18up},
            &g_{35}&=\frac q{3p},\\
            g_{44}&=\frac p{2v},
            &g_{55}&=\frac{2u}{p}.
            \end{aligned}
            $$

            The $(1,3,5)$ block is coupled, which is why a full inverse and curvature
            expansion are substantially heavier than in the round-sphere notebooks.
            """
        ),
        code(
            """
            def g_i_j : Matrix MathValue :=
              [| [| (3 * p^2 * (sin θ)^2 * u + 2 * v * p * (cos θ)^2 + q^2 * (cos θ)^2) / (18 * u * p)
                   , 0
                   , (-2 * v * p * cos θ - q^2 * cos θ) / (18 * u * p)
                   , 0
                   , (-q * cos θ) / (3 * p) |]
               , [| 0, p / 6, 0, 0, 0 |]
               , [| (-2 * v * p * cos θ - q^2 * cos θ) / (18 * u * p)
                   , 0
                   , (2 * v * p + q^2) / (18 * u * p)
                   , 0
                   , q / (3 * p) |]
               , [| 0, 0, 0, p / (2 * v), 0 |]
               , [| (-q * cos θ) / (3 * p), 0, q / (3 * p), 0, 2 * u / p |]
               |]_i_j
            """
        ),
        code("g_2_2"),
        code("g_4_4"),
        code("(g_1_3, g_3_1, g_1_5, g_5_1)"),
        markdown(
            r"""
            ## Connection and curvature pipeline

            The first-kind symbols require only derivatives of the displayed metric.
            Raising an index introduces the inverse of the coupled block.  The Riemann
            and Ricci definitions are nevertheless identical to the lower-dimensional
            examples:

            $$
            R^i{}_{jkl}=\partial_k\Gamma^i{}_{jl}-\partial_l\Gamma^i{}_{jk}
              +\Gamma^m{}_{jl}\Gamma^i{}_{mk}-\Gamma^m{}_{jk}\Gamma^i{}_{ml},
            \qquad
            \operatorname{Ric}_{ij}=R^m{}_{imj}.
            $$
            """
        ),
        code(
            """
            def g~i~j : Matrix MathValue := M.inverse g_#_#

            def Γ_i_j_k : Tensor MathValue :=
              (1 / 2) * (∂/∂ g_i_k x~j + ∂/∂ g_i_j x~k - ∂/∂ g_j_k x~i)

            def Γ~i_j_k : Tensor MathValue := withSymbols [m]
              g~i~m . Γ_m_j_k

            def R~i_j_k_l : Tensor MathValue := withSymbols [m]
              ∂/∂ Γ~i_j_l x~k - ∂/∂ Γ~i_j_k x~l
                + Γ~m_j_l . Γ~i_m_k - Γ~m_j_k . Γ~i_m_l

            def Ric_i_j : Matrix MathValue := withSymbols [m]
              sum (contract R~m_i_m_j)

            def einsteinResidual_i_j : Matrix MathValue := withSymbols [i, j]
              expandAll' (Ric_i_j -' 4 *' g_i_j)
            """
        ),
        code("Γ_2_2_4"),
        code("Γ_2_4_2"),
        markdown(
            r"""
            ## Interpretation and evaluation strategy

            The two sampled first-kind symbols come from the simple $g_{22}=p/6$
            entry and show the expected symmetry $\Gamma_{ijk}=\Gamma_{ikj}$.  The
            complete test is `einsteinResidual_#_#`; mathematically it is the zero
            matrix, so the scalar curvature is $5\cdot4=20$.

            Expanding all 25 residual entries involves the inverse coupled block and
            many rational simplifications.  It is intentionally not an automatic
            output cell: evaluate individual entries such as
            `einsteinResidual_2_2` when investigating the identity interactively.
            """
        ),
    ]


def _schwarzschild_cells() -> list[dict]:
    return [
        markdown(
            r"""
            # Riemann Curvature of the Schwarzschild Metric

            Outside a static spherical mass $M$, let

            $$
            A(r)=1-\frac{2GM}{c^2r}.
            $$

            With signature $(+---)$ and coordinates $(t,r,\theta,\phi)$, the line
            element is

            $$
            ds^2=A\,dt^2-A^{-1}dr^2-r^2d\theta^2-r^2\sin^2\theta\,d\phi^2.
            $$

            The metric is Ricci-flat but not Riemann-flat.  Selected components make
            that distinction visible without requesting a costly expansion of every
            curvature component.
            """
        ),
        markdown(
            r"""
            ## Metric and inverse

            The chart covers $r>0$ away from $A=0$.  The surface
            $r=2GM/c^2$ is a coordinate horizon in this chart, whereas $r=0$ will be
            detected by a curvature invariant.
            """
        ),
        code(
            """
            declare symbol G, M, c, t, r, θ, φ: MathValue

            def x : Vector MathValue := [| t, r, θ, φ |]
            def A : MathValue := `(c^2 * r - 2 * G * M) / (c^2 * r)

            def g_i_j : Matrix MathValue :=
              [| [| A, 0, 0, 0 |]
               , [| 0, -1 / A, 0, 0 |]
               , [| 0, 0, -r^2, 0 |]
               , [| 0, 0, 0, -r^2 * (sin θ)^2 |]
               |]_i_j

            def g~i~j : Matrix MathValue :=
              [| [| 1 / A, 0, 0, 0 |]
               , [| 0, -A, 0, 0 |]
               , [| 0, 0, -r^(-2), 0 |]
               , [| 0, 0, 0, -r^(-2) * (sin θ)^(-2) |]
               |]~i~j
            """
        ),
        code("A"),
        code("g_#_#"),
        code("g~#~#"),
        markdown(
            r"""
            ## Levi-Civita connection

            The connection is computed from the metric, rather than entered as a table.
            Angular components such as $\Gamma^\theta{}_{r\theta}=1/r$ and
            $\Gamma^\phi{}_{\theta\phi}=\cot\theta$ are especially compact checks.
            """
        ),
        code(
            """
            def Γ_i_j_k : Tensor MathValue :=
              (1 / 2) * (∂/∂ g_i_k x~j + ∂/∂ g_i_j x~k - ∂/∂ g_j_k x~i)

            def Γ~i_j_k : Tensor MathValue := withSymbols [m]
              g~i~m . Γ_m_j_k
            """
        ),
        code("Γ~3_2_3"),
        code("Γ~4_3_4"),
        markdown(
            r"""
            ## Riemann and Ricci tensors

            We use the same sign convention as the round-sphere notebooks.  The angular
            component $R^\theta{}_{\phi\theta\phi}$ is nonzero when $M\ne0$; a flat
            spherical-coordinate metric would make its radial and angular terms cancel.
            Ricci curvature is the contraction $R^m{}_{imj}$.
            """
        ),
        code(
            """
            def R~i_j_k_l : Tensor MathValue := withSymbols [m]
              expandAll
                (∂/∂ Γ~i_j_l x~k - ∂/∂ Γ~i_j_k x~l
                  + Γ~m_j_l . Γ~i_m_k - Γ~m_j_k . Γ~i_m_l)

            def Ric_i_j : Matrix MathValue := withSymbols [m]
              sum (contract R~m_i_m_j)

            def scalarCurvature : MathValue := withSymbols [i, j]
              g~i~j . Ric_i_j
            """
        ),
        code("expandAll (R~3_4_3_4)"),
        code("expandAll (Ric_1_1)"),
        markdown(
            r"""
            ## Interpretation

            The Riemann component records tidal curvature, while the Ricci component
            simplifies to zero, as required by the vacuum Einstein equations.  The
            coordinate-independent Kretschmann invariant is

            $$
            R_{abcd}R^{abcd}=\frac{48G^2M^2}{c^4r^6}.
            $$

            Thus curvature is finite at the Schwarzschild horizon but diverges at
            $r=0$.  The full invariant contraction is stated rather than made an output
            cell because expanding all four-index combinations is needlessly expensive
            for an interactive demonstration.
            """
        ),
    ]


def _flrw_cells() -> list[dict]:
    return [
        markdown(
            r"""
            # Riemann Curvature of the FLRW Metric

            The Friedmann--Lemaître--Robertson--Walker geometry models a homogeneous,
            isotropic universe.  In comoving coordinates $(w,r,\theta,\phi)$ and units
            $c=1$,

            $$
            ds^2=-dw^2+a(w)^2\left(
              \frac{dr^2}{1-Kr^2}+r^2d\theta^2+r^2\sin^2\theta\,d\phi^2
            \right).
            $$

            The scale factor $a(w)$ is left as an arbitrary symbolic function and $K$
            is the constant spatial-curvature parameter.
            """
        ),
        markdown(
            r"""
            ## Metric data

            Write $W(r)=(1-Kr^2)^{-1}$.  The inverse metric is entered explicitly so
            that selected connection and curvature components stay responsive.
            """
        ),
        code(
            """
            declare symbol w, r, θ, φ, K: MathValue

            def x : Vector MathValue := [| w, r, θ, φ |]
            def a : MathValue := function (w)

            def W (r: MathValue) : MathValue := 1 / `(1 - K * r^2)

            def g_i_j : Matrix MathValue :=
              [| [| -1, 0, 0, 0 |]
               , [| 0, a^2 * W r, 0, 0 |]
               , [| 0, 0, a^2 * r^2, 0 |]
               , [| 0, 0, 0, a^2 * r^2 * (sin θ)^2 |]
               |]_i_j

            def g~i~j : Matrix MathValue :=
              [| [| -1, 0, 0, 0 |]
               , [| 0, 1 / (a^2 * W r), 0, 0 |]
               , [| 0, 0, 1 / (a^2 * r^2), 0 |]
               , [| 0, 0, 0, 1 / (a^2 * r^2 * (sin θ)^2) |]
               |]~i~j
            """
        ),
        code("W r"),
        code("g_#_#"),
        code("g~#~#"),
        markdown(
            r"""
            ## Expansion enters the connection

            Time derivatives of the spatial metric generate Christoffel symbols
            proportional to $a'(w)$.  In particular, radial expansion appears in both
            $\Gamma^w{}_{rr}$ and $\Gamma^r{}_{wr}$.
            """
        ),
        code(
            """
            def Γ_i_j_k : Tensor MathValue :=
              (1 / 2) * (∂/∂ g_i_k x~j + ∂/∂ g_i_j x~k - ∂/∂ g_j_k x~i)

            def Γ~i_j_k : Tensor MathValue := withSymbols [m]
              g~i~m . Γ_m_j_k
            """
        ),
        code("Γ~1_2_2"),
        code("Γ~2_1_2"),
        markdown(
            r"""
            ## Riemann tensor and contractions

            Components mixing time and space measure the acceleration of the scale
            factor; purely spatial components combine $(a')^2$ with $K$.  The complete
            contractions are

            $$
            \operatorname{Ric}_{ij}=R^m{}_{imj},\qquad
            \mathcal R=g^{ij}\operatorname{Ric}_{ij}.
            $$
            """
        ),
        code(
            """
            def R~i_j_k_l : Tensor MathValue := withSymbols [m]
              ∂/∂ Γ~i_j_l x~k - ∂/∂ Γ~i_j_k x~l
                + Γ~m_j_l . Γ~i_m_k - Γ~m_j_k . Γ~i_m_l

            def Ric_i_j : Matrix MathValue := withSymbols [m]
              sum (contract R~m_i_m_j)

            def scalarCurvature : MathValue := withSymbols [i, j]
              expandAll' (g~i~j . Ric_i_j)
            """
        ),
        code("R~1_2_1_2"),
        code("R~2_3_2_3"),
        markdown(
            r"""
            ## Scalar curvature and interpretation

            With this convention, the expected scalar is

            $$
            \mathcal R
              =6\left(\frac{a''(w)}{a(w)}+
                \frac{a'(w)^2+K}{a(w)^2}\right)
              =\frac{6\bigl(a''a+(a')^2+K\bigr)}{a^2}.
            $$

            The selected Riemann components expose the two geometric ingredients:
            accelerated expansion and curvature of spatial slices.  Evaluating
            `scalarCurvature` asks the CAS to form and simplify the full contraction
            for an arbitrary function $a$ and can take several minutes, so it is
            deliberately a definition rather than an automatic output cell.
            """
        ),
    ]


def build() -> list[Path]:
    """Write this module's ten deterministic notebooks and return their paths."""

    written = [
        write_notebook("gaussian-curvature-of-surface", _surface_cells()),
    ]
    for dimension, sphere_name, angles in SPHERES:
        written.append(
            write_notebook(
                f"riemann-curvature-tensor-of-{sphere_name}",
                _sphere_cells(dimension, angles),
            )
        )
    written.extend(
        [
            write_notebook("riemann-curvature-tensor-of-T2", _torus_cells()),
            write_notebook("riemann-curvature-tensor-of-S2xS3", _s2xs3_cells()),
            write_notebook(
                "riemann-curvature-tensor-of-Schwarzschild-metric",
                _schwarzschild_cells(),
            ),
            write_notebook("riemann-curvature-tensor-of-FLRW-metric", _flrw_cells()),
        ]
    )
    return written


if __name__ == "__main__":
    for notebook_path in build():
        print(notebook_path)
