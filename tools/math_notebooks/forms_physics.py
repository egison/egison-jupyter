"""Build the differential-form, vector-analysis, and physics notebooks."""

from __future__ import annotations

from .common import code, markdown, write_notebook


def build_trigonometric_identities() -> None:
    write_notebook(
        "trigonometric-identities",
        [
            markdown(
                r"""
                # Trigonometric Identities from Complex Multiplication

                Euler's formula packages cosine and sine into one algebraic object,

                $$u(\alpha)=\cos\alpha+i\sin\alpha=e^{i\alpha}.$$

                Multiplying these objects lets the real and imaginary coefficients
                reveal several familiar identities.  This is a useful symbolic-computation
                pattern: perform one polynomial calculation and interpret its coefficients.
                """
            ),
            markdown(
                r"""
                ## Symbolic unit-circle elements

                We keep $\alpha$ and $\beta$ symbolic.  The expression `uMinusBeta`
                represents $u(-\beta)=\cos\beta-i\sin\beta$ without asking the
                simplifier to know parity rules for sine and cosine.
                """
            ),
            code(
                r"""
                declare symbol α, β : MathValue

                def uAlpha : MathValue := cos α + i * sin α
                def uBeta : MathValue := cos β + i * sin β
                def uMinusBeta : MathValue := cos β - i * sin β
                """
            ),
            markdown(
                r"""
                ## Angle-addition formulas

                The coefficients of $1$ and $i$ in $u(\alpha)u(\beta)$ are,
                respectively, $\cos(\alpha+\beta)$ and $\sin(\alpha+\beta)$.
                """
            ),
            code(
                r"""
                coefficients (uAlpha * uBeta) i
                """
            ),
            markdown(
                r"""
                Reading the two returned coefficients gives

                $$
                \cos(\alpha+\beta)=\cos\alpha\cos\beta-\sin\alpha\sin\beta,
                $$
                $$
                \sin(\alpha+\beta)=\sin\alpha\cos\beta+\cos\alpha\sin\beta.
                $$

                Adding $u(\alpha)u(\beta)$ and $u(\alpha)u(-\beta)$ isolates
                the product-to-sum combinations.
                """
            ),
            code(
                r"""
                coefficients (uAlpha * uBeta + uAlpha * uMinusBeta) i
                """
            ),
            markdown(
                r"""
                The result encodes $2\cos\alpha\cos\beta$ in its real part and
                $2\sin\alpha\cos\beta$ in its imaginary part.  Dividing by two
                and replacing the two products by $u(\alpha\pm\beta)$ yields the
                standard product-to-sum identities.

                ## Triple-angle formulas

                Cubing one unit-circle element performs all terms of the binomial
                expansion at once.
                """
            ),
            code(
                r"""
                coefficients (uAlpha ^ 3) i
                """
            ),
            markdown(
                r"""
                The real and imaginary components are

                $$\cos^3\alpha-3\cos\alpha\sin^2\alpha,$$
                $$3\cos^2\alpha\sin\alpha-\sin^3\alpha.$$

                Using $\sin^2\alpha=1-\cos^2\alpha$ in the first and
                $\cos^2\alpha=1-\sin^2\alpha$ in the second gives

                $$\cos(3\alpha)=4\cos^3\alpha-3\cos\alpha,$$
                $$\sin(3\alpha)=3\sin\alpha-4\sin^3\alpha.$$

                The essential point is that Egison's coefficient extraction turns
                complex multiplication into a transparent derivation, rather than
                merely checking a pre-stated identity.
                """
            ),
        ],
    )


def build_wedge_product() -> None:
    write_notebook(
        "wedge-product",
        [
            markdown(
                r"""
                # Wedge Product and Antisymmetrization

                Differential forms multiply with the alternating wedge product.
                For one-forms $a$ and $b$,

                $$(a\wedge b)_{ij}=\frac12(a_i b_j-a_j b_i),$$

                so $a\wedge b=-b\wedge a$ and $a\wedge a=0$.  Egison first
                constructs an indexed tensor product and then exposes the alternating
                differential-form representative through `dfNormalize`.
                """
            ),
            markdown(
                r"""
                ## Coordinate one-forms in $\mathbb R^3$

                In the ordered basis $(dx,dy,dz)$, each basis one-form is represented
                by a vector.  The ambient dimension and coordinates are included to
                make the geometric setting explicit.
                """
            ),
            code(
                r"""
                declare symbol x, y, z : MathValue

                def N : Integer := 3
                def params : Vector MathValue := [| x, y, z |]

                def dx : DiffForm Integer := [| 1, 0, 0 |]
                def dy : DiffForm Integer := [| 0, 1, 0 |]
                def dz : DiffForm Integer := [| 0, 0, 1 |]
                """
            ),
            markdown(
                r"""
                ## Raw indexed product

                The raw wedge expression retains the ordered component generated by
                the tensor operation.  Looking at it before normalization makes the
                representation convention visible.
                """
            ),
            code(
                r"""
                dx ∧ dy
                """
            ),
            markdown(
                r"""
                ## Alternating two-form

                Normalization distributes that component over the antisymmetric
                matrix.  The entries at $(1,2)$ and $(2,1)$ have opposite signs and
                carry the conventional factor $1/2$.
                """
            ),
            code(
                r"""
                dfNormalize (dx ∧ dy)
                """
            ),
            markdown(
                r"""
                Antisymmetrization also removes a repeated basis direction.  Although
                the intermediate indexed product $dz\wedge dz$ has a diagonal entry,
                its differential-form normalization is zero.
                """
            ),
            code(
                r"""
                dfNormalize (dz ∧ dz)
                """
            ),
            markdown(
                r"""
                Thus `dfNormalize` is not cosmetic: it projects an indexed tensor onto
                its alternating part.  Once normalized, the displayed tensors obey the
                geometric identities $dx\wedge dy=-dy\wedge dx$ and $dz\wedge dz=0$.
                """
            ),
        ],
    )


def build_exterior_derivative() -> None:
    write_notebook(
        "exterior-derivative",
        [
            markdown(
                r"""
                # Exterior Derivative and $d^2=0$

                The exterior derivative sends a $k$-form to a $(k+1)$-form.  On a
                scalar function it is the gradient one-form,

                $$df=\frac{\partial f}{\partial x^i},dx^i,$$

                and on all differential forms it satisfies the fundamental identity
                $d^2=0$.
                """
            ),
            markdown(
                r"""
                ## A coordinate-free implementation pattern

                Egison's tensor derivative can map the partial-derivative operator
                across the coordinate vector.  The polymorphic definition below works
                for a scalar or a tensor-valued expression.
                """
            ),
            code(
                r"""
                declare symbol x, y, z : MathValue

                def params : Vector MathValue := [| x, y, z |]

                def d {a} (X : a) : DiffForm a := !(flip ∂/∂) params X

                def f : MathValue := x ^ 2 + y ^ 2 + z ^ 2
                """
            ),
            markdown(
                r"""
                For $f=x^2+y^2+z^2$, the first exterior derivative is the radial
                gradient one-form $2x\,dx+2y\,dy+2z\,dz$.
                """
            ),
            code(
                r"""
                d f
                """
            ),
            markdown(
                r"""
                Applying the tensor derivative a second time first produces the raw
                Hessian.  This intermediate object has not yet been projected onto its
                alternating differential-form part.
                """
            ),
            code(
                r"""
                d (d f)
                """
            ),
            markdown(
                r"""
                The Hessian of a smooth scalar is symmetric, while a two-form is
                antisymmetric.  Their alternating projection therefore vanishes.
                """
            ),
            code(
                r"""
                dfNormalize (d (d f))
                """
            ),
            markdown(
                r"""
                This computation is the coordinate expression of $d^2f=0$: mixed
                partial derivatives cancel pairwise after antisymmetrization.  Showing
                both the Hessian and its normalized form separates ordinary tensor
                differentiation from the geometric exterior derivative.
                """
            ),
        ],
    )


def build_hodge_e3() -> None:
    write_notebook(
        "hodge-E3",
        [
            markdown(
                r"""
                # Hodge Star in Euclidean Three-Space

                A metric and an orientation identify $k$-forms with $(3-k)$-forms.
                In oriented Euclidean coordinates,

                $$\star dx=dy\wedge dz,\qquad
                  \star(dx\wedge dy)=dz.$$

                The Hodge star is where the metric enters differential-form calculus.
                """
            ),
            markdown(
                r"""
                ## Euclidean metric and basis forms

                We use the identity metric on $(x,y,z)$ and the standard orientation.
                The metric is typed as a matrix of symbolic mathematical values so the
                same definition pattern also works for nonconstant metrics.
                """
            ),
            code(
                r"""
                declare symbol x, y, z : MathValue

                def N : Integer := 3
                def params : Vector MathValue := [| x, y, z |]
                def g : Matrix MathValue :=
                  [| [| 1, 0, 0 |], [| 0, 1, 0 |], [| 0, 0, 1 |] |]

                def dx : DiffForm MathValue := [| 1, 0, 0 |]
                def dy : DiffForm MathValue := [| 0, 1, 0 |]
                def dz : DiffForm MathValue := [| 0, 0, 1 |]
                """
            ),
            markdown(
                r"""
                ## Definition of the Hodge star

                For a $k$-form $A$, the Levi-Civita tensor supplies the complementary
                indices, inverse metrics raise the contracted indices, and
                $\sqrt{|\det g|}$ supplies the volume density.
                """
            ),
            code(
                r"""
                def hodge (A : DiffForm MathValue) : DiffForm MathValue :=
                  let k := dfOrder A
                   in withSymbols [i, j]
                        sqrt (abs (M.det g_#_#)) *
                        foldl
                          (.)
                          ((ε' N k)_(i_1)..._(i_N) . A..._(j_1)..._(j_k))
                          (map (\n -> g~(i_n)~(j_n)) [1..k])
                """
            ),
            markdown(
                r"""
                A one-form becomes a two-form supported in the complementary oriented
                plane.
                """
            ),
            code(
                r"""
                hodge dx
                """
            ),
            markdown(
                r"""
                Conversely, the oriented area form in the $xy$-plane becomes the
                one-form normal to that plane.
                """
            ),
            code(
                r"""
                hodge (wedge dx dy)
                """
            ),
            markdown(
                r"""
                The two outputs are the component versions of
                $\star dx=dy\wedge dz$ and $\star(dx\wedge dy)=dz$.  In three-dimensional
                Euclidean signature, applying $\star$ twice returns a one-form or a
                two-form with positive sign; changing the metric signature changes that
                sign, as the Minkowski-space notebook demonstrates.
                """
            ),
        ],
    )


def build_hodge_minkowski() -> None:
    write_notebook(
        "hodge-minkowski",
        [
            markdown(
                r"""
                # Hodge Star in Minkowski Spacetime

                Electromagnetism is naturally expressed with differential forms on
                spacetime.  With metric signature $(-,+,+,+)$, the Hodge star maps
                two-forms to two-forms, but time-like basis elements introduce signs:

                $$\star(dt\wedge dx)=-dy\wedge dz,\qquad
                  \star(dy\wedge dz)=dt\wedge dx.$$
                """
            ),
            markdown(
                r"""
                ## Lorentzian metric

                The determinant has negative sign, so the volume density uses
                $\sqrt{|\det g|}$.  Raising a time index contributes the additional
                minus sign visible in the result.
                """
            ),
            code(
                r"""
                declare symbol t, x, y, z : MathValue

                def N : Integer := 4
                def params : Vector MathValue := [| t, x, y, z |]
                def g : Matrix MathValue :=
                  [| [| -1, 0, 0, 0 |]
                   , [| 0, 1, 0, 0 |]
                   , [| 0, 0, 1, 0 |]
                   , [| 0, 0, 0, 1 |] |]

                def dt : DiffForm MathValue := [| 1, 0, 0, 0 |]
                def dx : DiffForm MathValue := [| 0, 1, 0, 0 |]
                def dy : DiffForm MathValue := [| 0, 0, 1, 0 |]
                def dz : DiffForm MathValue := [| 0, 0, 0, 1 |]
                """
            ),
            markdown(
                r"""
                ## Metric-dependent duality

                The definition is the same contraction used in Euclidean space.  Only
                the dimension and metric have changed.
                """
            ),
            code(
                r"""
                def hodge (A : DiffForm MathValue) : DiffForm MathValue :=
                  let k := dfOrder A
                   in withSymbols [i, j]
                        sqrt (abs (M.det g_#_#)) *
                        foldl
                          (.)
                          ((ε' N k)_(i_1)..._(i_N) . A..._(j_1)..._(j_k))
                          (map (\n -> g~(i_n)~(j_n)) [1..k])
                """
            ),
            markdown(
                r"""
                First dualize a two-form containing the time direction.
                """
            ),
            code(
                r"""
                hodge (wedge dt dx)
                """
            ),
            markdown(
                r"""
                A purely spatial area form dualizes to a time-space area form.
                """
            ),
            code(
                r"""
                hodge (wedge dy dz)
                """
            ),
            markdown(
                r"""
                These signs imply $\star^2=-1$ on two-forms for this Lorentzian
                convention.  They are also the signs that exchange electric and
                magnetic components when the electromagnetic field tensor is dualized.
                """
            ),
        ],
    )


def build_hodge_laplacian_polar() -> None:
    write_notebook(
        "hodge-laplacian-polar",
        [
            markdown(
                r"""
                # Hodge Laplacian in Polar Coordinates

                This notebook derives the scalar Hodge Laplacian from the metric and
                differential-form operators.  For polar coordinates $(r,\theta)$ with
                $r>0$,

                $$g=dr^2+r^2d\theta^2.$$

                With the codifferential convention used below, the result is the
                negative of the usual positive-coordinate Laplace operator.
                """
            ),
            markdown(
                r"""
                ## Polar metric

                Both the covariant and contravariant metrics carry explicit tensor
                indices.  This lets Egison contract them automatically in the Hodge
                formula.
                """
            ),
            code(
                r"""
                declare symbol r, θ : MathValue

                def N : Integer := 2
                def x : Vector MathValue := [| r, θ |]

                def g_i_j : Matrix MathValue :=
                  [| [| 1, 0 |], [| 0, r ^ 2 |] |]_i_j
                def g~i~j : Matrix MathValue :=
                  [| [| 1, 0 |], [| 0, r ^ (-2) |] |]~i~j
                """
            ),
            code(
                r"""
                g_#_#
                """
            ),
            markdown(
                r"""
                ## Exterior derivative and Hodge star

                The Hodge star combines the Levi-Civita tensor, the inverse metric,
                and the volume density $\sqrt{|g|}=r$.
                """
            ),
            code(
                r"""
                def d (A : Tensor MathValue) : Tensor MathValue :=
                  !(flip ∂/∂) x A

                def hodge (A : Tensor MathValue) : Tensor MathValue :=
                  let k := dfOrder A
                   in withSymbols [i, j]
                        sqrt (M.det g_#_#) *
                        foldl
                          (.)
                          ((subrefs A (map 1#j_$1 (between 1 k))) .
                           (subrefs (ε' N k) (map 1#i_$1 (between 1 N))))
                          (map 1#g~(i_$1)~(j_$1) [1..k])
                """
            ),
            markdown(
                r"""
                ## Codifferential and Laplacian

                The codifferential is the metric adjoint of $d$ and can be written in
                terms of two Hodge stars.  The degree test selects the appropriate
                endpoint formula for zero- and top-degree forms.
                """
            ),
            code(
                r"""
                def δ (A : Tensor MathValue) : Tensor MathValue :=
                  let k := dfOrder A
                   in (-1) ^ (N * (k + 1) + 1) * (hodge (d (hodge A)))

                def Δ (A : Tensor MathValue) : Tensor MathValue :=
                  match (dfOrder A) as integer with
                  | #0 -> δ (d A)
                  | #N -> d (δ A)
                  | _  -> d (δ A) + δ (d A)

                def f : MathValue := function (r, θ)
                """
            ),
            markdown(
                r"""
                Applying the operator to an arbitrary scalar function leaves its
                derivatives symbolic, so the coordinate formula is visible directly.
                """
            ),
            code(
                r"""
                Δ f
                """
            ),
            markdown(
                r"""
                The displayed expression is

                $$
                \Delta f=-\left(
                  \frac{\partial^2f}{\partial r^2}
                  +\frac1r\frac{\partial f}{\partial r}
                  +\frac1{r^2}\frac{\partial^2f}{\partial\theta^2}
                \right).
                $$

                The $1/r$ and $1/r^2$ terms are not inserted by hand: they arise from
                the determinant and inverse metric inside the Hodge star.
                """
            ),
        ],
    )


def build_hodge_laplacian_spherical() -> None:
    write_notebook(
        "hodge-laplacian-spherical",
        [
            markdown(
                r"""
                # Hodge Laplacian in Spherical Coordinates

                In $(r,\theta,\phi)$ coordinates, the Euclidean metric is

                $$ds^2=dr^2+r^2d\theta^2+r^2\sin^2\theta\,d\phi^2.$$

                We build $d$, $\star$, and the codifferential from this metric.  With
                the codifferential convention used below, the scalar result is the
                negative of the usual positive-coordinate Laplace operator.
                """
            ),
            markdown(
                r"""
                ## Spherical metric

                The determinant is $r^4\sin^2\theta$, while the inverse metric contains
                the angular scale factors $r^{-2}$ and
                $(r^2\sin^2\theta)^{-1}$.
                """
            ),
            code(
                r"""
                declare symbol r, θ, φ : MathValue

                def N : Integer := 3
                def x : Vector MathValue := [| r, θ, φ |]

                def g_i_j : Matrix MathValue :=
                  [| [| 1, 0, 0 |]
                   , [| 0, r ^ 2, 0 |]
                   , [| 0, 0, r ^ 2 * (sin θ) ^ 2 |] |]_i_j
                def g~i~j : Matrix MathValue :=
                  [| [| 1, 0, 0 |]
                   , [| 0, 1 / r ^ 2, 0 |]
                   , [| 0, 0, 1 / (r ^ 2 * (sin θ) ^ 2) |] |]~i~j
                """
            ),
            code(
                r"""
                g_#_#
                """
            ),
            markdown(
                r"""
                ## Differential-form operators

                The Hodge star raises the form indices with $g^{ij}$ and contracts them
                against the three-dimensional Levi-Civita tensor.
                """
            ),
            code(
                r"""
                def d (A : Tensor MathValue) : Tensor MathValue :=
                  !(flip ∂/∂) x A

                def hodge (A : DiffForm MathValue) : DiffForm MathValue :=
                  let k := dfOrder A
                   in withSymbols [i, j]
                        sqrt (abs (M.det g_#_#)) *
                        foldl
                          (.)
                          ((ε' N k)_(i_1)..._(i_N) . A..._(j_1)..._(j_k))
                          (map (\n -> g~(i_n)~(j_n)) [1..k])

                def δ (A : DiffForm MathValue) : DiffForm MathValue :=
                  let k := dfOrder A
                   in ((-1) ^ (N * (k + 1) + 1)) * hodge (d (hodge A))
                """
            ),
            markdown(
                r"""
                The Hodge Laplacian is $d\delta+\delta d$, with shorter endpoint
                formulas for scalars and volume forms.
                """
            ),
            code(
                r"""
                def Δ (A : DiffForm MathValue) : DiffForm MathValue :=
                  match dfOrder A as integer with
                  | #0 -> δ (d A)
                  | #N -> d (δ A)
                  | _  -> d (δ A) + δ (d A)

                def f : MathValue := function (r, θ, φ)
                """
            ),
            code(
                r"""
                Δ f
                """
            ),
            markdown(
                r"""
                After simplification, the output is

                $$
                \Delta f=-\left(
                f_{rr}+\frac{2}{r}f_r
                +\frac1{r^2}f_{\theta\theta}
                +\frac{\cos\theta}{r^2\sin\theta}f_\theta
                +\frac1{r^2\sin^2\theta}f_{\phi\phi}
                \right).
                $$

                Each coordinate-dependent coefficient follows from the metric; the
                calculation contains no spherical-coordinate Laplacian formula as an
                input.
                """
            ),
        ],
    )


def build_curvature_form() -> None:
    write_notebook(
        "curvature-form",
        [
            markdown(
                r"""
                # Curvature Two-Form on the Sphere

                The Riemann tensor can be computed directly from Christoffel symbols or
                assembled as the curvature of the connection one-form.  Cartan's second
                structure equation is

                $$\Omega^i{}_j=d\omega^i{}_j+\omega^i{}_k\wedge\omega^k{}_j,$$

                with $\Omega^i{}_j=\tfrac12R^i{}_{jkl}\,dx^k\wedge dx^l$.
                """
            ),
            markdown(
                r"""
                ## Round metric on $S^2$

                For a sphere of radius $r$ with coordinates $(\theta,\phi)$,

                $$g_{ij}=\operatorname{diag}(r^2,r^2\sin^2\theta).$$
                """
            ),
            code(
                r"""
                declare symbol r, θ, φ : MathValue

                def x : Vector MathValue := [| θ, φ |]
                def g_i_j : Matrix MathValue :=
                  [| [| r ^ 2, 0 |], [| 0, r ^ 2 * (sin θ) ^ 2 |] |]_i_j
                def g~i~j : Matrix MathValue :=
                  [| [| 1 / r ^ 2, 0 |]
                   , [| 0, 1 / (r ^ 2 * (sin θ) ^ 2) |] |]~i~j
                """
            ),
            code(
                r"""
                g_#_#
                """
            ),
            markdown(
                r"""
                ## Direct Riemann tensor

                The Levi-Civita connection follows from metric compatibility and zero
                torsion.  Egison's repeated symbolic indices perform the contraction
                over $m$.
                """
            ),
            code(
                r"""
                def Γ_j_l_k : Tensor MathValue :=
                  (1 / 2) *
                    (∂/∂ g_j_l x~k + ∂/∂ g_j_k x~l - ∂/∂ g_k_l x~j)

                def Γ~i_k_l : Tensor MathValue :=
                  withSymbols [j] g~i~j . Γ_j_l_k

                def R~i_j_k_l : Tensor MathValue := withSymbols [m]
                  ∂/∂ Γ~i_j_l x~k - ∂/∂ Γ~i_j_k x~l
                  + Γ~m_j_l . Γ~i_m_k - Γ~m_j_k . Γ~i_m_l
                """
            ),
            code(
                r"""
                R~#_#_1_2
                """
            ),
            markdown(
                r"""
                ## Cartan's curvature form

                Regard the last Christoffel index as the one-form index.  The exterior
                derivative adds one form index, and `antisymmetrize` projects the result
                onto a genuine two-form.
                """
            ),
            code(
                r"""
                def d (t : Tensor MathValue) : Tensor MathValue :=
                  !(flip ∂/∂) x t

                def ω~i_j : Matrix MathValue := Γ~i_j_#

                def Ω~i_j : Tensor MathValue := withSymbols [k]
                  antisymmetrize (d ω~i_j + ω~i_k ∧ ω~k_j)
                """
            ),
            code(
                r"""
                Ω~#_#_1_2
                """
            ),
            markdown(
                r"""
                The curvature-form component is one half of the corresponding direct
                Riemann component, exactly as
                $\Omega^i{}_j=\tfrac12R^i{}_{jkl}dx^k\wedge dx^l$ requires.  The two
                computational paths therefore agree while exposing different geometry:
                the first uses coordinate indices, and the second treats curvature as
                the field strength of a connection.
                """
            ),
        ],
    )


def build_vector_analysis() -> None:
    write_notebook(
        "vector-analysis",
        [
            markdown(
                r"""
                # Vector Analysis with Tensor Derivatives

                Gradient, Jacobian, divergence, and curl are different arrangements of
                the same partial derivatives.  Egison's tensor notation makes those
                arrangements explicit and keeps the symbolic expressions readable.
                """
            ),
            markdown(
                r"""
                ## Scalar and vector fields

                We use a polynomial scalar field and a vector field on $\mathbb R^3$ so
                every derivative remains symbolic but has an easily interpretable form.
                """
            ),
            code(
                r"""
                declare symbol x, y, z : MathValue

                def coords : Vector MathValue := [| x, y, z |]
                def f : MathValue := x ^ 2 * y + y ^ 2 * z + z ^ 2 * x
                def A : Vector MathValue := [| x * y, y * z, z * x |]
                """
            ),
            markdown(
                r"""
                ## Gradient

                Differentiating a scalar with respect to the coordinate vector produces
                the covector of first partial derivatives.
                """
            ),
            code(
                r"""
                ∂/∂ f coords
                """
            ),
            markdown(
                r"""
                ## Jacobian

                A vector of derivative operators applied to a vector field produces the
                full Jacobian matrix.  Rows correspond to differentiation by
                $x$, $y$, and $z$.
                """
            ),
            code(
                r"""
                [| (\e -> ∂/∂ e x), (\e -> ∂/∂ e y), (\e -> ∂/∂ e z) |] A
                """
            ),
            markdown(
                r"""
                ## Divergence

                Divergence contracts the derivative index with the vector-component
                index:

                $$\nabla\cdot A=\partial_x A_x+\partial_y A_y+\partial_z A_z.$$
                """
            ),
            code(
                r"""
                div A coords
                """
            ),
            markdown(
                r"""
                ## Curl

                Curl contracts the Jacobian with the Levi-Civita tensor,
                $(\nabla\times A)_i=\varepsilon_{ijk}\partial_jA_k$.
                """
            ),
            code(
                r"""
                rot A coords
                """
            ),
            markdown(
                r"""
                ## A local series view

                Tensor calculus and series expansion share the same symbolic derivative
                machinery.  Expanding $f$ in $x$ about zero treats $y$ and $z$ as
                parameters.
                """
            ),
            code(
                r"""
                take 4 (taylorExpansion f x 0)
                """
            ),
            markdown(
                r"""
                The gradient retains every first derivative, the divergence selects the
                Jacobian trace, and the curl selects its antisymmetric part.  These are
                therefore not unrelated operators: they are distinct contractions and
                symmetries of one derivative tensor.
                """
            ),
        ],
    )


def build_yang_mills_u1() -> None:
    write_notebook(
        "yang-mills-equation-of-U1-gauge-theory",
        [
            markdown(
                r"""
                # $U(1)$ Yang--Mills Theory as Electromagnetism

                For an Abelian gauge field, the connection is a spacetime one-form $A$
                and its curvature is the electromagnetic two-form

                $$F=dA.$$

                Maxwell's equations become the Bianchi identity $dF=0$ and the source
                equation $\delta F=J$.  In vacuum, $J=0$.
                """
            ),
            markdown(
                r"""
                ## Minkowski spacetime and form operators

                We use signature $(-,+,+,+)$.  The codifferential is built from the
                Hodge star and the exterior derivative, so all metric signs enter in a
                single place.
                """
            ),
            code(
                r"""
                declare symbol t, x, y, z : MathValue

                def N : Integer := 4
                def coords : Vector MathValue := [| t, x, y, z |]
                def g : Matrix MathValue :=
                  [| [| -1, 0, 0, 0 |]
                   , [| 0, 1, 0, 0 |]
                   , [| 0, 0, 1, 0 |]
                   , [| 0, 0, 0, 1 |] |]

                def d (X : Tensor MathValue) : Tensor MathValue :=
                  !(flip ∂/∂) coords X

                def hodge (A : DiffForm MathValue) : DiffForm MathValue :=
                  let k := dfOrder A
                   in withSymbols [i, j]
                        sqrt (abs (M.det g_#_#)) *
                        foldl
                          (.)
                          ((ε' N k)_(i_1)..._(i_N) . A..._(j_1)..._(j_k))
                          (map (\n -> g~(i_n)~(j_n)) [1..k])

                def δ (A : DiffForm MathValue) : DiffForm MathValue :=
                  let k := dfOrder A
                   in (-1) ^ (N * k + 1) * hodge (d (hodge A))
                """
            ),
            markdown(
                r"""
                A quick basis check fixes the Lorentzian orientation and sign convention:
                $\star(dt\wedge dx)=-dy\wedge dz$.
                """
            ),
            code(
                r"""
                hodge (wedge [| 1, 0, 0, 0 |] [| 0, 1, 0, 0 |])
                """
            ),
            markdown(
                r"""
                ## Gauge potential and curvature

                Let $A=\varphi\,dt+A_x\,dx+A_y\,dy+A_z\,dz$, with arbitrary symbolic
                component functions.  Antisymmetrizing $dA$ exposes the electric and
                magnetic field-strength combinations.
                """
            ),
            code(
                r"""
                def ϕ : MathValue := function (t, x, y, z)
                def Ax : MathValue := function (t, x, y, z)
                def Ay : MathValue := function (t, x, y, z)
                def Az : MathValue := function (t, x, y, z)

                def potential : DiffForm MathValue := [| ϕ, Ax, Ay, Az |]
                """
            ),
            code(
                r"""
                dfNormalize (d potential)
                """
            ),
            markdown(
                r"""
                ## Maxwell tensor

                To display the field equations in their familiar variables, define the
                antisymmetric tensor $F_{\mu\nu}$ from symbolic electric and magnetic
                components.  Egison stores a differential two-form as
                $\tfrac12F_{\mu\nu}dx^\mu\wedge dx^\nu$, so the full antisymmetric
                component matrix carries an explicit factor of one half.
                """
            ),
            code(
                r"""
                def Ex : MathValue := function (t, x, y, z)
                def Ey : MathValue := function (t, x, y, z)
                def Ez : MathValue := function (t, x, y, z)
                def Bx : MathValue := function (t, x, y, z)
                def By : MathValue := function (t, x, y, z)
                def Bz : MathValue := function (t, x, y, z)

                def F : DiffForm MathValue :=
                  (1 / 2) *
                    [| [| 0, Ex, Ey, Ez |]
                     , [| -Ex, 0, -Bz, By |]
                     , [| -Ey, Bz, 0, -Bx |]
                     , [| -Ez, -By, Bx, 0 |] |]
                """
            ),
            markdown(
                r"""
                The dual Bianchi expression packages $\nabla\cdot B=0$ and
                $\nabla\times E=-\partial_tB$.
                """
            ),
            code(
                r"""
                hodge (d F)
                """
            ),
            markdown(
                r"""
                The codifferential packages Gauss's law and the Ampere--Maxwell law.
                Setting this vector equal to a current one-form gives $\delta F=J$.
                """
            ),
            code(
                r"""
                δ F
                """
            ),
            markdown(
                r"""
                The one-half component convention now agrees with
                `dfNormalize (d potential)`.  The derivative combinations are the
                homogeneous and sourced Maxwell equations.  This is the Abelian
                $U(1)$ Yang--Mills system, where the nonlinear $A\wedge A$ term vanishes.
                """
            ),
        ],
    )


def build_euler_form_s2() -> None:
    write_notebook(
        "euler-form-of-S2",
        [
            markdown(
                r"""
                # Euler Form of the Two-Sphere

                The Euler class of an oriented rank-two tangent bundle is represented
                by a curvature two-form.  For the round sphere,

                $$\int_{S^2} e(TS^2)=\chi(S^2)=2.$$

                We compute the metric from the embedding, transform the connection to
                an orthonormal frame, and apply Cartan's curvature equation.
                """
            ),
            markdown(
                r"""
                ## Embedding and induced metric

                The radius-$r$ sphere is parametrized by $(\theta,\phi)$.  Dot products
                of its coordinate tangent vectors produce the metric rather than taking
                it as an input.
                """
            ),
            code(
                r"""
                declare symbol r, θ, φ : MathValue

                def x : Vector MathValue := [| θ, φ |]
                def X : Vector MathValue :=
                  [| r * sin θ * cos φ
                   , r * sin θ * sin φ
                   , r * cos θ |]

                def e_i_j : Matrix MathValue := ∂/∂ X_j x~i
                def g_i_j : Matrix MathValue :=
                  generateTensor (\[a, b] -> V.* e_a_# e_b_#) [2, 2]
                def g~i~j : Matrix MathValue := M.inverse g_#_#
                """
            ),
            code(
                r"""
                g_#_#
                """
            ),
            markdown(
                r"""
                ## Levi-Civita connection and orthonormal frame

                The diagonal vielbein rescales the coordinate basis by $r$ and
                $r\sin\theta$.  Under a frame change $A$, the connection transforms as

                $$\omega=A^{-1}\omega_0A+A^{-1}dA.$$
                """
            ),
            code(
                r"""
                def Γ_i_j_k : Tensor MathValue :=
                  (1 / 2) *
                    (∂/∂ g_i_k x~j + ∂/∂ g_i_j x~k - ∂/∂ g_j_k x~i)

                def Γ~i_j_k : Tensor MathValue := withSymbols [m]
                  g~i~m . Γ_m_j_k

                def A : Matrix MathValue :=
                  [| [| 1 / r, 0 |], [| 0, 1 / (r * sin θ) |] |]

                def d (t : Tensor MathValue) : Tensor MathValue :=
                  !(flip ∂/∂) x t

                def ω0~i_j : Matrix MathValue := Γ~i_j_#
                def ω~i_j : Tensor MathValue := withSymbols [a, b]
                  (M.inverse A)~i_a . ω0~a_b . A~b_j
                  + (M.inverse A)~i_a . d A~a_j
                """
            ),
            markdown(
                r"""
                ## Curvature and Euler form

                Cartan's second equation gives $\Omega$.  In two dimensions the
                Pfaffian reduces to the difference of the two off-diagonal curvature
                components.
                """
            ),
            code(
                r"""
                def Ω~i_j : Tensor MathValue := withSymbols [k]
                  antisymmetrize (d ω~i_j + ω~i_k ∧ ω~k_j)

                def eulerForm : Tensor MathValue :=
                  (1 / (4 * π)) * withSymbols [t1, t2]
                    (Ω~1_2_t1_t2 - Ω~2_1_t1_t2)
                """
            ),
            code(
                r"""
                eulerForm
                """
            ),
            markdown(
                r"""
                The upper tensor component is

                $$e_{12}=\frac{\sin\theta}{4\pi}.$$

                A full antisymmetric tensor stores both $e_{12}$ and $e_{21}$, so
                the corresponding oriented differential-form density is

                $$e(TS^2)=\frac{\sin\theta}{2\pi}\,d\theta\wedge d\phi.$$

                Therefore

                $$\int_0^{2\pi}\!\int_0^\pi
                  \frac{\sin\theta}{2\pi}\,d\theta\,d\phi=2,$$

                recovering the Euler characteristic of the sphere.  The radius cancels,
                illustrating that the Euler number is topological rather than metric-size
                dependent.
                """
            ),
        ],
    )


def build_euler_form_t2() -> None:
    write_notebook(
        "euler-form-of-T2",
        [
            markdown(
                r"""
                # Euler Form of the Two-Torus

                A torus has regions of positive and negative Gaussian curvature, but
                their total cancels:

                $$\int_{T^2}e(TT^2)=\chi(T^2)=0.$$

                This notebook computes the local Euler form from an embedded torus and
                makes that cancellation explicit.
                """
            ),
            markdown(
                r"""
                ## Embedded torus and metric

                Let $a$ be the tube radius and $b$ the distance from the tube center to
                the symmetry axis.  The opaque quotes around $a\cos\theta+b$ preserve a
                compact symbolic atom during intermediate matrix computations.
                """
            ),
            code(
                r"""
                declare symbol θ, φ, a, b : MathValue

                def x : Vector MathValue := [| θ, φ |]
                def X : Vector MathValue :=
                  [| `(a * cos θ + b) * cos φ
                   , `(a * cos θ + b) * sin φ
                   , a * sin θ |]

                def e_i_j : Matrix MathValue := ∂/∂ X_j x~i
                def g_i_j : Matrix MathValue :=
                  generateTensor (\[u, v] -> V.* e_u_# e_v_#) [2, 2]
                def g~i~j : Matrix MathValue := M.inverse g_#_#
                """
            ),
            code(
                r"""
                g_#_#
                """
            ),
            markdown(
                r"""
                ## Connection in an orthonormal frame

                The vielbein removes the coordinate scale factors.  As on the sphere,
                the inhomogeneous $A^{-1}dA$ term is essential when changing frames.
                """
            ),
            code(
                r"""
                def Γ_i_j_k : Tensor MathValue :=
                  (1 / 2) *
                    (∂/∂ g_i_k x~j + ∂/∂ g_i_j x~k - ∂/∂ g_j_k x~i)

                def Γ~i_j_k : Tensor MathValue := withSymbols [m]
                  g~i~m . Γ_m_j_k

                def A : Matrix MathValue :=
                  [| [| 1 / a, 0 |]
                   , [| 0, 1 / `(a * cos θ + b) |] |]

                def d (t : Tensor MathValue) : Tensor MathValue :=
                  !(flip ∂/∂) x t

                def ω0~i_j : Matrix MathValue := Γ~i_j_#
                def ω~i_j : Tensor MathValue := withSymbols [u, v]
                  (M.inverse A)~i_u . ω0~u_v . A~v_j
                  + (M.inverse A)~i_u . d A~u_j
                """
            ),
            markdown(
                r"""
                The nonzero connection coefficient changes sign across the torus and
                drives the sign-changing curvature.
                """
            ),
            code(
                r"""
                ω~1_2_2
                """
            ),
            markdown(
                r"""
                ## Curvature and Euler form

                We explicitly antisymmetrize the two form indices after applying
                Cartan's equation, then take the rank-two Pfaffian.
                """
            ),
            code(
                r"""
                def Ω~i_j : Tensor MathValue := withSymbols [k]
                  antisymmetrize (d ω~i_j + ω~i_k ∧ ω~k_j)

                def eulerForm : Tensor MathValue :=
                  (1 / (4 * π)) * withSymbols [t1, t2]
                    (Ω~1_2_t1_t2 - Ω~2_1_t1_t2)
                """
            ),
            code(
                r"""
                eulerForm
                """
            ),
            markdown(
                r"""
                The upper tensor component is $\cos\theta/(4\pi)$; including its
                antisymmetric partner gives the oriented density
                $\cos\theta\,d\theta\wedge d\phi/(2\pi)$.  Its integral over one full
                meridian vanishes:

                $$\int_0^{2\pi}\cos\theta\,d\theta=0.$$

                Hence the positive outer curvature and negative inner curvature cancel,
                giving $\chi(T^2)=0$ independently of $a$ and $b$.
                """
            ),
        ],
    )


def build_chern_form_cp1() -> None:
    write_notebook(
        "chern-form-of-CP1",
        [
            markdown(
                r"""
                # First Chern Form on $\mathbb{CP}^1$

                A complex line bundle is characterized by the curvature of a unitary
                connection.  On an affine chart of $\mathbb{CP}^1$, use the complex
                coordinate

                $$u=r e^{2\pi i\theta},\qquad \bar u=r e^{-2\pi i\theta}.$$

                We compute a Fubini--Study connection, its curvature, and the normalized
                first Chern form.
                """
            ),
            markdown(
                r"""
                ## Polar chart and connection one-form

                The chart variables are $(r,\theta)$ with $r\ge0$ and
                $0\le\theta<1$.  The local connection is

                $$\omega=\frac{\bar u\,du}{1+u\bar u}.$$
                """
            ),
            code(
                r"""
                declare symbol r, θ : MathValue

                def params : Vector MathValue := [| r, θ |]
                def u : MathValue := r * e ^ (2 * π * i * θ)
                def ū : MathValue := r * e ^ ((-2) * π * i * θ)

                def d (X : MathValue) : DiffForm MathValue :=
                  !(flip ∂/∂) params X

                def ω : DiffForm MathValue := ū * d u / '(1 + u * ū)
                """
            ),
            code(
                r"""
                ω
                """
            ),
            markdown(
                r"""
                ## Curvature two-form

                For a line bundle the connection is Abelian, so $\omega\wedge\omega=0$
                and $\Omega=d\omega$.  We display its antisymmetric component matrix
                explicitly.
                """
            ),
            code(
                r"""
                def ωr : MathValue := ω_1
                def ωθ : MathValue := ω_2
                def Ωrθ : MathValue :=
                  (∂/∂ ωθ r - ∂/∂ ωr θ) / 2
                def Ω : DiffForm MathValue :=
                  [| [| 0, Ωrθ |], [| -Ωrθ, 0 |] |]
                """
            ),
            code(
                r"""
                Ω
                """
            ),
            markdown(
                r"""
                ## First Chern form

                With the orientation and connection convention used here,

                $$c_1=\frac{\Omega}{-2\pi i}.$$
                """
            ),
            code(
                r"""
                def c1Form : DiffForm MathValue := Ω / ((-2) * π * i)
                """
            ),
            code(
                r"""
                c1Form
                """
            ),
            markdown(
                r"""
                The full antisymmetric form contributes twice its upper component, so
                its oriented density is

                $$-\frac{2r}{(1+r^2)^2}\,dr\wedge d\theta.$$

                Integrating over $r\in[0,\infty)$ and $\theta\in[0,1)$ gives

                $$\int_0^\infty\frac{-2r}{(1+r^2)^2}\,dr=-1.$$

                Thus this convention describes the degree $-1$ line bundle.  Reversing
                the orientation or using the dual connection reverses the Chern number.
                """
            ),
        ],
    )


def main() -> None:
    builders = [
        build_trigonometric_identities,
        build_wedge_product,
        build_exterior_derivative,
        build_hodge_e3,
        build_hodge_minkowski,
        build_hodge_laplacian_polar,
        build_hodge_laplacian_spherical,
        build_curvature_form,
        build_vector_analysis,
        build_yang_mills_u1,
        build_euler_form_s2,
        build_euler_form_t2,
        build_chern_form_cp1,
    ]
    for builder in builders:
        builder()


if __name__ == "__main__":
    main()
