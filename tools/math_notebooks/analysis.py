"""Build the mathematical-analysis notebooks."""

from .common import code, markdown, write_notebook


def build_eulers_formula() -> None:
    write_notebook(
        "eulers-formula",
        [
            markdown(
                r"""
                # Euler's Formula

                Euler's formula links the exponential function to circular motion:

                $$
                e^{ix}=\cos x+i\sin x.
                $$

                We verify the identity coefficient by coefficient.  Egison differentiates
                symbolic expressions to generate the Maclaurin terms on both sides.
                """
            ),
            markdown(
                r"""
                ## Maclaurin expansion of the exponential

                For a function $F$, the term of degree $n$ at the origin is

                $$
                \frac{F^{(n)}(0)}{n!}x^n.
                $$

                We first ask for the first eight terms of $e^{ix}$.
                """
            ),
            code(
                """
                declare symbol x : MathValue
                """
            ),
            code(
                """
                take 8 (taylorExpansion (e^(i * x)) x 0)
                """
            ),
            markdown(
                r"""
                ## Real and imaginary parts

                The even powers occur in $\cos x$, while the odd powers occur in
                $i\sin x$.  Computing the two series separately makes this parity
                split visible.
                """
            ),
            code(
                """
                take 8 (taylorExpansion (cos x) x 0)
                """
            ),
            code(
                """
                take 8 (taylorExpansion (i * sin x) x 0)
                """
            ),
            markdown(
                r"""
                ## Coefficient-by-coefficient comparison

                Adding the two lists must reproduce the exponential series through
                every displayed order.
                """
            ),
            code(
                """
                take 8
                  (map2 (+)
                    (taylorExpansion (cos x) x 0)
                    (taylorExpansion (i * sin x) x 0))
                """
            ),
            markdown(
                r"""
                The final list is identical to the expansion of $e^{ix}$.  The
                calculation exhibits Euler's formula as a formal power-series
                identity, without substituting a numerical value for $x$.
                """
            ),
        ],
    )


def fourier_definitions() -> str:
    return """
        declare symbol x, n : MathValue

        def f (x : MathValue) : MathValue := x

        def cosinePrimitive (k : MathValue) : MathValue :=
          x * sin (k * x) / k + cos (k * x) / k^2

        def sinePrimitive (k : MathValue) : MathValue :=
          (- x) * cos (k * x) / k + sin (k * x) / k^2
        """


def fourier_coefficients() -> str:
    return """
        def cosineCoefficients : [MathValue] :=
          map
            (\k ->
              let primitive := cosinePrimitive k
               in (substitute [(x, π)] primitive - substitute [(x, - π)] primitive) / π)
            nats

        def sineCoefficients : [MathValue] :=
          map
            (\k ->
              let primitive := sinePrimitive k
               in (substitute [(x, π)] primitive - substitute [(x, - π)] primitive) / π)
            nats
        """


def build_fourier_series() -> None:
    write_notebook(
        "fourier-series",
        [
            markdown(
                r"""
                # Fourier Series of a Sawtooth Wave

                Consider the $2\pi$-periodic extension of $f(x)=x$ on
                $-\pi<x<\pi$.  Its Fourier series is

                $$
                f(x)\sim \frac{a_0}{2}
                  +\sum_{k=1}^{\infty}a_k\cos(kx)
                  +\sum_{k=1}^{\infty}b_k\sin(kx).
                $$

                Egison symbolically evaluates the coefficient integrals and builds
                the first terms of the series.
                """
            ),
            markdown(
                r"""
                ## Symbolic antiderivatives

                The coefficients use

                $$
                a_k=\frac1\pi\int_{-\pi}^{\pi}x\cos(kx)\,dx,
                \qquad
                b_k=\frac1\pi\int_{-\pi}^{\pi}x\sin(kx)\,dx.
                $$

                Integration by parts gives explicit primitives for
                $x\cos(kx)$ and $x\sin(kx)$.  We define those formulas directly,
                keeping the notebook independent of optional integration libraries.
                """
            ),
            code(fourier_definitions()),
            code(
                """
                sinePrimitive n
                """
            ),
            markdown(
                r"""
                ## Fourier coefficients

                The sawtooth is odd, so every cosine coefficient is zero.  The sine
                coefficients are $b_k=2(-1)^{k+1}/k$.
                """
            ),
            code(fourier_coefficients()),
            code(
                """
                take 10 cosineCoefficients
                """
            ),
            code(
                """
                take 10 sineCoefficients
                """
            ),
            markdown(
                r"""
                ## Reconstructing the series

                Multiplying each $b_k$ by $\sin(kx)$ gives the successive Fourier
                terms.
                """
            ),
            code(
                """
                def fourierTerms : [MathValue] :=
                  map (\(k, b) -> b * sin (k * x)) (zip nats sineCoefficients)
                """
            ),
            code(
                """
                take 10 fourierTerms
                """
            ),
            markdown(
                r"""
                Thus

                $$
                x=2\sum_{k=1}^{\infty}\frac{(-1)^{k+1}}{k}\sin(kx)
                \qquad(-\pi<x<\pi).
                $$

                The separate parity and coefficient cells make clear why no cosine
                terms survive.
                """
            ),
        ],
    )


def build_leibniz_formula() -> None:
    write_notebook(
        "leibniz-formula",
        [
            markdown(
                r"""
                # Leibniz Formula from a Fourier Series

                The Leibniz series

                $$
                \frac{\pi}{4}=1-\frac13+\frac15-\frac17+\cdots
                $$

                follows by evaluating the Fourier series of the sawtooth
                $f(x)=x$ at $x=\pi/2$.  This notebook derives the coefficients
                symbolically before making that substitution.
                """
            ),
            markdown(
                r"""
                ## The sawtooth and its coefficients

                Since $f$ is odd, only sine terms occur:

                $$
                x=\sum_{k=1}^{\infty}b_k\sin(kx),\qquad
                b_k=\frac1\pi\int_{-\pi}^{\pi}x\sin(kx)\,dx.
                $$
                """
            ),
            code(fourier_definitions()),
            code(fourier_coefficients()),
            code(
                """
                take 10 sineCoefficients
                """
            ),
            markdown(
                r"""
                ## Fourier terms

                Egison now combines each coefficient with its basis function.
                """
            ),
            code(
                """
                def fourierTerms : [MathValue] :=
                  map (\(k, b) -> b * sin (k * x)) (zip nats sineCoefficients)
                """
            ),
            code(
                """
                take 10 fourierTerms
                """
            ),
            markdown(
                r"""
                ## Evaluate at $x=\pi/2$

                Even harmonics vanish, while successive odd harmonics alternate in
                sign.  We encode the exact four-step pattern

                $$
                \sin(k\pi/2)=1,0,-1,0,\ldots
                $$

                before dividing the Fourier terms by two.  Thus the identity
                $\pi/2=2(1-1/3+1/5-\cdots)$ gives the desired series.
                """
            ),
            code(
                """
                def sinAtHalfPi (k : Integer) : MathValue :=
                  if isEven k
                    then 0
                    else (-1) ^ (i.quotient (k - 1) 2)

                def leibnizTerms : [MathValue] :=
                  map
                    (\\(k, b) -> b * sinAtHalfPi k / 2)
                    (zip nats sineCoefficients)
                """
            ),
            code(
                """
                take 10 leibnizTerms
                """
            ),
            markdown(
                r"""
                Reading the nonzero entries yields
                $1,-1/3,1/5,-1/7,\ldots$.  Their infinite sum is $\pi/4$;
                the zeros record the even Fourier modes that vanish at $\pi/2$.
                """
            ),
        ],
    )


def build_partial_derivative_order() -> None:
    write_notebook(
        "order-of-partial-derivative",
        [
            markdown(
                r"""
                # The Order of Partial Differentiation

                For a sufficiently smooth function, mixed partial derivatives
                commute.  We illustrate Clairaut's theorem with

                $$
                f(x,y,z)=\frac{x^5y^3}{z},
                $$

                differentiating once with respect to each variable in several
                orders.
                """
            ),
            markdown(
                r"""
                ## Define the function

                The explicit type annotation makes the symbolic domain clear to
                the Egison kernel.
                """
            ),
            code(
                """
                declare symbol x, y, z : MathValue

                def f (x : MathValue) (y : MathValue) (z : MathValue) : MathValue :=
                  x^5 * y^3 / z
                """
            ),
            code(
                """
                f x y z
                """
            ),
            markdown(
                r"""
                ## A first mixed derivative

                Differentiating in the order $x$, then $y$, then $z$ should give

                $$
                \partial_z\partial_y\partial_x f
                  =-\frac{15x^4y^2}{z^2}.
                $$
                """
            ),
            code(
                """
                ∂/∂ (∂/∂ (∂/∂ (f x y z) x) y) z
                """
            ),
            markdown(
                r"""
                ## Permuting the order

                We repeat the calculation with $z,y,x$ and $y,z,x$.  Equality of
                all three outputs is the computational form of Clairaut's theorem
                on the region $z\ne0$.
                """
            ),
            code(
                """
                ∂/∂ (∂/∂ (∂/∂ (f x y z) z) y) x
                """
            ),
            code(
                """
                ∂/∂ (∂/∂ (∂/∂ (f x y z) y) z) x
                """
            ),
            markdown(
                r"""
                Every order produces the same rational expression.  The example
                also shows that Egison keeps the variables of differentiation
                explicit instead of encoding the order in auxiliary function names.
                """
            ),
        ],
    )


def build_laplacian_hessian_jacobian() -> None:
    write_notebook(
        "laplacian-hessian-jacobian",
        [
            markdown(
                r"""
                # Laplacian, Hessian, and Jacobian

                All three operators are assembled from the same array of partial
                derivatives.  For a scalar $f$ and vector map $F$,

                $$
                (\operatorname{Hess}f)_{ij}=\partial_i\partial_j f,
                \qquad
                \Delta f=\operatorname{tr}(\operatorname{Hess}f),
                \qquad
                J_F=(\partial_jF_i)_{ij}.
                $$
                """
            ),
            markdown(
                r"""
                ## Coordinates and test fields

                We use $f=x^2+y^2+z^2$ and
                $F=(x^2,y^2,z^2)$.  Both have diagonal derivative matrices, which
                makes the expected answers easy to inspect.
                """
            ),
            code(
                """
                declare symbol x, y, z : MathValue

                def parameters : Vector MathValue := [| x, y, z |]
                def scalarField : MathValue := x^2 + y^2 + z^2
                def vectorField : Vector MathValue := [| x^2, y^2, z^2 |]
                """
            ),
            code(
                """
                ∂/∂ scalarField parameters
                """
            ),
            markdown(
                r"""
                ## Hessian and Laplacian

                `generateTensor` supplies the two free matrix indices.  Taking the
                trace of the resulting Hessian implements the Euclidean Laplacian.
                """
            ),
            code(
                """
                def hessian (f : MathValue) : Matrix MathValue :=
                  generateTensor
                    (\[a, b] -> ∂/∂ (∂/∂ f parameters_a) parameters_b)
                    [3, 3]

                def laplacian (f : MathValue) : MathValue := trace (hessian f)
                """
            ),
            code(
                """
                hessian scalarField
                """
            ),
            code(
                """
                laplacian scalarField
                """
            ),
            markdown(
                r"""
                ## Jacobian matrix and determinant

                The same indexed construction differentiates each component of
                $F$.  Its determinant measures the local volume scaling.
                """
            ),
            code(
                """
                def jacobian (v : Vector MathValue) : Matrix MathValue :=
                  generateTensor
                    (\[a, b] -> ∂/∂ v_a parameters_b)
                    [3, 3]
                """
            ),
            code(
                """
                jacobian vectorField
                """
            ),
            code(
                """
                M.det (jacobian vectorField)
                """
            ),
            markdown(
                r"""
                The outputs are $2I_3$, $6$, and $8xyz$, respectively.  They show
                how tensor generation, contraction, and determinant calculation
                express three familiar multivariable operators in a uniform way.
                """
            ),
        ],
    )


def polar_geometry(dimension: int) -> tuple[str, str, str, str]:
    if dimension == 2:
        setup = """
            declare symbol r, θ : MathValue

            def q : Vector MathValue := [| r, θ |]
            def g_i_j : Matrix MathValue :=
              [| [| 1, 0 |], [| 0, r^2 |] |]_i_j
            def g~i~j : Matrix MathValue :=
              [| [| 1, 0 |], [| 0, r^(-2) |] |]~i~j

            def f : MathValue := function (r, θ)
            """
        cartesian = """
            def X : MathValue := r * cos θ
            def Y : MathValue := r * sin θ
            def u : MathValue := function (X, Y)

            def uR : MathValue := ∂/∂ u r
            def uRR : MathValue := ∂/∂ (∂/∂ u r) r
            def uΘΘ : MathValue := ∂/∂ (∂/∂ u θ) θ
            """
        cartesian_result = "uRR + uR / r + uΘΘ / r^2"
        expected = r"""
            $$
            \Delta f=\frac{\partial^2f}{\partial r^2}
              +\frac1r\frac{\partial f}{\partial r}
              +\frac1{r^2}\frac{\partial^2f}{\partial\theta^2}.
            $$
            """
    else:
        setup = """
            declare symbol r, θ, φ : MathValue

            def q : Vector MathValue := [| r, θ, φ |]
            def g_i_j : Matrix MathValue :=
              [| [| 1, 0, 0 |]
               , [| 0, r^2, 0 |]
               , [| 0, 0, r^2 * (sin θ)^2 |]
               |]_i_j
            def g~i~j : Matrix MathValue := M.inverse g_#_#

            def f : MathValue := function (r, θ, φ)
            """
        cartesian = """
            def X : MathValue := r * sin θ * cos φ
            def Y : MathValue := r * sin θ * sin φ
            def Z : MathValue := r * cos θ
            def u : MathValue := function (X, Y, Z)

            def uR : MathValue := ∂/∂ u r
            def uRR : MathValue := ∂/∂ (∂/∂ u r) r
            def uΘ : MathValue := ∂/∂ u θ
            def uΘΘ : MathValue := ∂/∂ (∂/∂ u θ) θ
            def uΦΦ : MathValue := ∂/∂ (∂/∂ u φ) φ
            """
        cartesian_result = """
            uRR + 2 * uR / r + uΘΘ / r^2
              + cos θ * uΘ / (r^2 * sin θ)
              + uΦΦ / (r^2 * (sin θ)^2)
            """
        expected = r"""
            $$
            \Delta f=\frac{\partial^2f}{\partial r^2}
              +\frac2r\frac{\partial f}{\partial r}
              +\frac1{r^2}\frac{\partial^2f}{\partial\theta^2}
              +\frac{\cos\theta}{r^2\sin\theta}\frac{\partial f}{\partial\theta}
              +\frac1{r^2\sin^2\theta}\frac{\partial^2f}{\partial\phi^2}.
            $$
            """
    return setup, cartesian, cartesian_result, expected


def build_polar_laplacian(dimension: int) -> None:
    is_plane = dimension == 2
    slug = "polar-laplacian-2d" if is_plane else "polar-laplacian-3d"
    title = "Laplacian in Polar Coordinates" if is_plane else "Laplacian in Spherical Coordinates"
    coordinate_name = "polar" if is_plane else "spherical"
    cartesian_name = "two" if is_plane else "three"
    setup, cartesian, cartesian_result, expected = polar_geometry(dimension)

    write_notebook(
        slug,
        [
            markdown(
                f"""
                # {title}

                The Euclidean Laplacian has a coordinate-independent meaning, but
                its formula changes with the coordinates.  We derive the
                {coordinate_name}-coordinate expression from the metric and then
                verify it by the multivariable chain rule.
                """
            ),
            markdown(
                (r"""
                ## Coordinate metric

                The line element is

                $$ds^2=dr^2+r^2d\theta^2$$
                """ if is_plane else r"""
                ## Coordinate metric

                The line element is

                $$ds^2=dr^2+r^2d\theta^2+r^2\sin^2\theta\,d\phi^2.$$
                """)
                + "\nThe metric and its inverse are represented as indexed tensors."
            ),
            code(setup),
            code(
                """
                g_#_#
                """
            ),
            markdown(
                r"""
                ## Covariant derivation

                For a scalar field, the Laplace--Beltrami operator can be written

                $$
                \Delta f=g^{ij}\partial_i\partial_jf
                   -g^{ij}\Gamma^k{}_{ij}\partial_kf.
                $$

                Egison contracts the repeated tensor indices in precisely this
                formula.
                """
            ),
            code(
                """
                def Γ_i_j_k : Tensor MathValue :=
                  (1 / 2) *
                    (∂/∂ g_i_k q~j + ∂/∂ g_i_j q~k - ∂/∂ g_j_k q~i)

                def Γ~i_j_k : Tensor MathValue := withSymbols [m]
                  g~i~m . Γ_m_j_k

                def laplacian : MathValue := withSymbols [i, j, k]
                  g~i~j . ∂/∂ (∂/∂ f q~j) q~i
                    - g~i~j . Γ~k_i_j . ∂/∂ f q~k
                """
            ),
            markdown("## Result\n\n" + expected),
            code(
                """
                laplacian
                """
            ),
            markdown(
                f"""
                ## Chain-rule verification

                Finally we regard a Cartesian function of {cartesian_name}
                variables as a function of the new coordinates.  Expanding the
                displayed coordinate formula should cancel every mixed derivative
                and leave the Cartesian Laplacian.
                """
            ),
            code(cartesian),
            code(cartesian_result),
            markdown(
                (r"""
                The expanded result is $u_{XX}+u_{YY}$, confirming that the
                $r^{-1}u_r$ term compensates for the changing angular scale.
                """ if is_plane else r"""
                The expanded result is $u_{XX}+u_{YY}+u_{ZZ}$.  The first-derivative
                terms are exactly the corrections produced by the changing radial
                and angular scale factors.
                """)
            ),
        ],
    )


def build() -> None:
    build_eulers_formula()
    build_fourier_series()
    build_leibniz_formula()
    build_partial_derivative_order()
    build_laplacian_hessian_jacobian()
    build_polar_laplacian(2)
    build_polar_laplacian(3)


if __name__ == "__main__":
    build()
