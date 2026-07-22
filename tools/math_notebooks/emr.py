"""Build notebooks for the EMR paper computations."""

from __future__ import annotations

from .common import code, markdown, write_notebook


def _highest_power_cells() -> list[dict]:
    return [
        markdown(
            r"""
            # Highest-Power Coefficient in the EMR Curvature Formula

            This notebook reproduces the finite-dimensional computation behind
            Theorem 3.4 of *Diffeomorphism Groups of Circle Bundles over Integral
            Symplectic Manifolds*.  The program alternates over all permutations
            and contracts copies of the standard complex structure.

            The complete research code is available in
            [EMR-Paper-Computation](https://github.com/egisatoshi/EMR-Paper-Computation).
            """
        ),
        markdown(
            r"""
            ## Standard complex structure

            On a real vector space of dimension $2k$, let

            $$
            J=\begin{pmatrix}0&I_k\\-I_k&0\end{pmatrix}.
            $$

            The notebook uses $k=2$ for a quick interactive calculation.  The
            final section records the larger computations with exactly the same
            definitions.
            """
        ),
        code(
            r"""
            def k := 2

            def J :=
              generateTensor
                (\match as list integer with
                   | [$i, #(i + k)] -> 1
                   | [$i, #(i - k)] -> -1
                   | _ -> 0)
                [2 * k, 2 * k]
            """
        ),
        code("J"),
        code("withSymbols [a, b, c] J_a~c . J_c~b"),
        markdown(
            r"""
            ## Alternating product

            Let $S_k$ be the signed sum of products

            $$
            S_k=\sum_{\sigma\in S_{2k}}\operatorname{sgn}(\sigma)
                \prod_{i=1}^{k}J_{\sigma(2i-1),\sigma(2i)}.
            $$

            `evenAndOddPermutations` supplies the two signs separately.
            """
        ),
        code(
            r"""
            def S :=
              let (es, os) := evenAndOddPermutations (2 * k) in
                sum (map (\σ -> product (map (\i -> J_(σ (2 * i - 1))_(σ (2 * i))) (between 1 k))) es) -
                sum (map (\σ -> product (map (\i -> J_(σ (2 * i - 1))_(σ (2 * i))) (between 1 k))) os)
            """
        ),
        code("S"),
        markdown(
            r"""
            ## Curvature coefficient

            The highest power of the bundle parameter $p$ is built from

            $$
            T_{abc}{}^d=-J_{bc}J_a{}^d+J_{ac}J_b{}^d
                         +2J_{ab}J_c{}^d.
            $$

            The indices $a_0,\ldots,a_{k-1}$ form a cyclic chain.  Tensor product
            followed by `.` contracts that chain, while the outer fold adds the
            even and odd permutation contributions.
            """
        ),
        code(
            r"""
            def T_a_b_c~d :=
              -1 * J_b_c . J_a~d +
              J_a_c . J_b~d +
              2 * J_a_b . J_c~d

            def S' :=
              withSymbols [a]
                let (es, os) := evenAndOddPermutations (2 * k) in
                  (\xs -> foldl (+) (head xs) (tail xs))
                    (map
                      (\σ ->
                        (\xs -> foldl (.) (head xs) (tail xs))
                          (map (\i -> T_(σ (2 * i - 1))_(σ (2 * i))_(a_(modulo i k))~(a_(i - 1))) (between 1 k)))
                      es) -
                  (\xs -> foldl (+) (head xs) (tail xs))
                    (map
                      (\σ ->
                        (\xs -> foldl (.) (head xs) (tail xs))
                          (map (\i -> T_(σ (2 * i - 1))_(σ (2 * i))_(a_(modulo i k))~(a_(i - 1))) (between 1 k)))
                      os)
            """
        ),
        code("S'"),
        markdown(
            r"""
            ## Higher dimensions

            The same program gives

            $$
            \begin{array}{c|rr}
            k&S_k&S'_k\\ \hline
            2&-8&192\\
            3&-48&0\\
            4&384&61440
            \end{array}
            $$

            On Egison 5.1.0 the full $k=4$ run takes about 25 minutes.  Keeping
            the interactive notebook at $k=2$ makes every cell quick to rerun;
            changing the first definition to `def k := 4` performs the complete
            Theorem 3.4 computation without any other code changes.
            """
        ),
    ]


def _thurston_cells() -> list[dict]:
    return [
        markdown(
            r"""
            # Wodzicki–Chern–Simons Invariant on the Thurston Example

            This notebook reproduces the symbolic computation in Section 4 of
            *Diffeomorphism Groups of Circle Bundles over Integral Symplectic
            Manifolds*.  It builds the metric, curvature, and lifted curvature
            tensor and then reduces the Wodzicki–Chern–Simons integrand to a
            compact rational expression.

            The original research program is maintained in
            [EMR-Paper-Computation](https://github.com/egisatoshi/EMR-Paper-Computation).
            """
        ),
        markdown(
            r"""
            ## Thurston metric

            Write $\beta=1+\theta_2-\theta_2^2$.  The metric and inverse metric
            below are expressed in the coordinate frame
            $(\theta_1,\theta_2,\theta_3,\theta_4)$.  Quoting the two recurring
            polynomial expressions keeps the intermediate tensor calculation
            compact.
            """
        ),
        code(
            r"""
            declare symbol θ₁, θ₂, θ₃, θ₄, κ, p

            def x~i := [| θ₁, θ₂, θ₃, θ₄ |]~i
            def β := `(1 + θ₂ - θ₂^2)

            def g_i_j :=
              [|[| 1, 0, 0, 0 |],
                [| 0, 1, 0, 0 |],
                [| 0, 0, κ / sqrt β, (-1 * θ₂ * κ) / sqrt β |],
                [| 0, 0, (-1 * θ₂ * κ) / sqrt β, (`(1 + θ₂) * κ) / sqrt β |]|]

            def g~i~j :=
              [|[| 1, 0, 0, 0 |],
                [| 0, 1, 0, 0 |],
                [| 0, 0, `(1 + θ₂) / (κ * sqrt β), θ₂ / (sqrt β * κ) |],
                [| 0, 0, θ₂ / (sqrt β * κ), 1 / (sqrt β * κ) |]|]
            """
        ),
        code("g_#_#"),
        code("withSymbols [i, j, k] g_i_j . g~j~k"),
        markdown(
            r"""
            ## Levi-Civita connection and curvature

            Egison's symbolic tensor indices transcribe the usual formulas

            $$
            \Gamma^c{}_{ab}=\frac12g^{ce}
              (\partial_ag_{be}+\partial_bg_{ae}-\partial_eg_{ab}),
            $$

            followed by $R_{ijk}{}^l$.  Repeated upper and lower indices are
            contracted by `.`.
            """
        ),
        code(
            r"""
            def Γ~c_a_b := withSymbols [e]
              (1 / 2) * g~c~e . (∂/∂ g_b_e x~a + ∂/∂ g_a_e x~b - ∂/∂ g_a_b x~e)

            def R_i_j_k~l := withSymbols [a]
              ∂/∂ Γ~l_j_k x~i - ∂/∂ Γ~l_i_k x~j
                + Γ~l_i_a . Γ~a_j_k - Γ~l_j_a . Γ~a_i_k

            def R_i_j_k_l := withSymbols [a] R_i_j_k~a . g_a_l
            """
        ),
        code("Γ~1_1_1"),
        markdown(
            r"""
            ## Complex structure and lifted curvature

            The complex structure $J$ and its covariant derivative determine the
            curvature $R'$ on the circle bundle.  The first coordinate is the
            fibre direction; the remaining four coordinates belong to the
            Thurston base.
            """
        ),
        code(
            r"""
            def J_a_b :=
              [|[| 0, 1, 0, 0 |],
                [| -1, 0, 0, 0 |],
                [| 0, 0, 0, κ |],
                [| 0, 0, -1 * κ, 0 |]|]

            def J_a~c := withSymbols [b] J_a_b . g~b~c

            def ∇J_m_a_b := withSymbols [n]
              ∂/∂ J_a_b x~m + Γ~n_m_a . J_n_b + Γ~n_m_b . J_a_n

            def ∇J~m_a_b := withSymbols [t] ∇J_t_a_b . g~t~m
            def ∇J_m~a_b := withSymbols [t] ∇J_m_t_b . g~t~a
            def ∇J_m_a~b := withSymbols [t] ∇J_m_a_t . g~t~b

            def δ :=
              generateTensor
                (\match as list integer with
                   | [$n, #n] -> 1
                   | [_, _] -> 0)
                [5, 5]
            """
        ),
        code(
            r"""
            def R'{_i_j}_k~l : Tensor MathValue :=
              generateTensor
                (\match as list integer with
                   | [#1, #1, _, _] -> 0
                   | [_, _, #1, #1] -> 0
                   | [#1, $b, #1, $d] -> -1 * p^2 * δ~(b - 1)_(d - 1)
                   | [$a, #1, #1, $d] ->      p^2 * δ~(a - 1)_(d - 1)
                   | [#1, $b, $c, #1] ->      p^2 * g_(b - 1)_(c - 1)
                   | [$a, #1, $c, #1] -> -1 * p^2 * g_(a - 1)_(c - 1)
                   | [#1, $b, $c, $d] -> -1 * p * ∇J_(b - 1)_(c - 1)~(d - 1)
                   | [$a, #1, $c, $d] ->      p * ∇J_(a - 1)_(c - 1)~(d - 1)
                   | [$a, $b, #1, $d] -> -1 * p * ∇J~(d - 1)_(a - 1)_(b - 1)
                   | [$a, $b, $c, #1] ->      p * ∇J_(c - 1)_(a - 1)_(b - 1)
                   | [$a, $b, $c, $d] -> R_(a - 1)_(b - 1)_(c - 1)~(d - 1)
                                         - p^2 * J_(b - 1)_(c - 1) * J_(a - 1)~(d - 1)
                                         + p^2 * J_(a - 1)_(c - 1) * J_(b - 1)~(d - 1)
                                         + 2 * p^2 * J_(a - 1)_(b - 1) * J_(c - 1)~(d - 1))
                [5, 5, 5, 5]
            """
        ),
        markdown(
            r"""
            ## Wodzicki–Chern–Simons contraction

            The alternating contraction contains three copies of $R'$.  Its raw
            result uses negative powers of the quoted atom $\beta$.  Multiplying
            by $16\beta^8$ clears those Laurent denominators.  A Gröbner basis for
            the defining quote relations then gives a canonical polynomial normal
            form, after which the denominator is restored.
            """
        ),
        code(
            r"""
            def S := withSymbols [i, j, k]
              let (es, os) := evenAndOddPermutations 5 in
                sum (map (\σ -> R'_(σ 1)_j_1~i . R'_(σ 2)_(σ 3)_k~j . R'_(σ 4)_(σ 5)_i~k) es) -
                sum (map (\σ -> R'_(σ 1)_j_1~i . R'_(σ 2)_(σ 3)_k~j . R'_(σ 4)_(σ 5)_i~k) os)

            def quoteGb :=
              groebnerBasis ['(1 + θ₂ - θ₂^2 - β), '(1 + θ₂ - `(1 + θ₂))]

            def sSimplified := polyNF quoteGb (16 * β^8 * S) / (16 * β^8)
            """
        ),
        code("sSimplified"),
        code(
            r"""
            def sClosedForm :=
              p^2 * κ * (-25 - 640 * p^2 * β^2 + 3072 * p^4 * β^4) / (16 * β^4)

            sSimplified = sClosedForm
            """
        ),
        markdown(
            r"""
            ## Result

            Egison reduces the full contraction to

            $$
            S=192p^6\kappa-\frac{40p^4\kappa}{\beta^2}
              -\frac{25p^2\kappa}{16\beta^4}
             =\frac{p^2\kappa(-25-640p^2\beta^2+3072p^4\beta^4)}
                    {16\beta^4}.
            $$

            Thus the expression previously simplified with an external computer
            algebra system is now calculated and normalized entirely by Egison.
            """
        ),
    ]


def build() -> None:
    write_notebook("emr-highest-power-coefficient", _highest_power_cells())
    write_notebook("emr-thurston-wcs-invariant", _thurston_cells())


def main() -> None:
    build()


if __name__ == "__main__":
    main()
