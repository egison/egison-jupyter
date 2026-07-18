"""Build the algebra and elementary-number-theory demonstration notebooks."""

from __future__ import annotations

from .common import code, markdown, write_notebook


def quadratic_equation() -> list[dict]:
    return [
        markdown(
            r"""
            # Solving a Quadratic Equation

            For

            $$
            ax^2+bx+c=0,\qquad a\ne0,
            $$

            the two roots are

            $$
            x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}.
            $$

            Rather than entering roots separately for each example, the Egison
            program reads the coefficients of a polynomial, constructs its
            discriminant, and applies one typed symbolic solver.
            """
        ),
        markdown(
            r"""
            ## Coefficients and the discriminant

            Egison's coefficients function returns coefficients in ascending
            degree order. Thus the pattern $[a_0,a_1,a_2]$ recognizes
            $a_2x^2+a_1x+a_0$. The helper keeps the cleared-denominator
            discriminant $b^2-4ac$ intact and explicitly groups the denominator
            as $2a$.
            """
        ),
        code(
            """
            declare symbol x, a, b, c: MathValue

            def solveQuadraticCoefficientsDemo
              (a : MathValue)
              (b : MathValue)
              (c : MathValue)
              : (MathValue, MathValue) :=
              let discriminant := b ^ 2 - 4 * a * c
               in ( ((- b) + sqrt discriminant) / (2 * a)
                  , ((- b) - sqrt discriminant) / (2 * a) )

            def solveQuadraticDemo
              (f : MathValue)
              (x : MathValue)
              : (MathValue, MathValue) :=
              match coefficients f x as list mathValue with
                | [$a_0, $a_1, $a_2] ->
                  solveQuadraticCoefficientsDemo a_2 a_1 a_0
            """
        ),
        markdown(
            r"""
            ## A cyclotomic example

            The polynomial $x^2+x+1$ has discriminant $-3$. Its roots are the
            two primitive cube roots of unity.
            """
        ),
        code(
            """
            solveQuadraticDemo (x ^ 2 + x + 1) x
            """
        ),
        markdown(
            r"""
            ## The symbolic formula

            Leaving $a$, $b$, and $c$ symbolic exposes the usual discriminant
            without any special formatting code.
            """
        ),
        code(
            """
            solveQuadraticDemo (a * x ^ 2 + b * x + c) x
            """
        ),
        markdown(
            r"""
            ## A useful rescaling

            Writing the middle coefficient as $2b$ gives the equivalent compact
            form

            $$
            x=\frac{-b\pm\sqrt{b^2-ac}}{a}.
            $$
            """
        ),
        code(
            """
            solveQuadraticDemo (a * x ^ 2 + 2 * b * x + c) x
            """
        ),
        markdown(
            r"""
            ## Takeaway

            Pattern matching and the typed helper separate the calculation into
            two transparent stages: read the polynomial coefficients, then form
            the discriminant and both signs of its square root. The displayed
            answers are produced from each input polynomial rather than inserted
            as precomputed outputs.
            """
        ),
    ]


def cubic_equation() -> list[dict]:
    return [
        markdown(
            r"""
            # Solving a Cubic Equation

            Cardano's method begins by translating a monic cubic to the
            depressed form

            $$
            y^3+py+q=0.
            $$

            If $y=(s_1+s_2)/3$, then $s_1^3$ and $s_2^3$ are the roots of

            $$
            t^2+27qt-27p^3=0.
            $$

            The three choices are obtained with the cube root of unity
            $\omega=(-1+i\sqrt3)/2$.
            """
        ),
        markdown(
            r"""
            ## Cardano's construction in Egison

            The first match clause handles the depressed cubic. The second
            performs the translation $x=y-b/3$, and the last divides by the
            leading coefficient. A small typed quadratic helper keeps the
            notebook self-contained.
            """
        ),
        code(
            """
            declare symbol x, a, b, c, d, p, q: MathValue

            def quadraticRoots
              (a : MathValue)
              (b : MathValue)
              (c : MathValue)
              : (MathValue, MathValue) :=
              ( ((- b) + sqrt (b ^ 2 - 4 * a * c)) / (2 * a)
              , ((- b) - sqrt (b ^ 2 - 4 * a * c)) / (2 * a) )

            def omega : MathValue := ((-1) + i * sqrt 3) / 2

            def cubicFormula : MathValue -> MathValue -> (MathValue, MathValue, MathValue) := cF

            def cF (f : MathValue) (x : MathValue) : (MathValue, MathValue, MathValue) :=
              match coefficients f x as list mathValue with
                | [$a_0, $a_1, $a_2, $a_3] -> cF' a_3 a_2 a_1 a_0

            def cF'
              (a : MathValue)
              (b : MathValue)
              (c : MathValue)
              (d : MathValue)
              : (MathValue, MathValue, MathValue) :=
              match (a, b, c, d) as (mathValue, mathValue, mathValue, mathValue) with
                | (#1, #0, $p, $q) ->
                  let (s1, s2) := (2)#(rt 3 $1, rt 3 $2)
                                     (quadraticRoots 1 (27 * q) ((-27) * p ^ 3))
                   in ( (s1 + s2) / 3
                      , (omega ^ 2 * s1 + omega * s2) / 3
                      , (omega * s1 + omega ^ 2 * s2) / 3 )
                | (#1, _, _, _) ->
                  (3)#($1 - b / 3, $2 - b / 3, $3 - b / 3)
                    (withSymbols [x, y]
                      cF
                        (substitute
                          [(x, y - b / 3)]
                          (x ^ 3 + b * x ^ 2 + c * x + d))
                        y)
                | (_, _, _, _) -> cF' 1 (b / a) (c / a) (d / a)
            """
        ),
        markdown(
            r"""
            ## The depressed cubic

            Keeping $p$ and $q$ symbolic makes Cardano's radicals visible in
            the output. The three tuple entries differ only by powers of
            $\omega$.
            """
        ),
        code(
            """
            cF (x ^ 3 + p * x + q) x
            """
        ),
        markdown(
            r"""
            ## Translation in action

            The next polynomial is written in factored form so that its roots
            are known in advance. Egison expands it, extracts its coefficients,
            depresses it, and reconstructs all three roots.
            """
        ),
        code(
            """
            cF ((x - 1) * (x - 2) * (x - 3)) x
            """
        ),
        markdown(
            r"""
            ## General leading coefficient

            The same function accepts a fully symbolic non-monic cubic
            $ax^3+bx^2+cx+d$. Its first action is normalization by $a$.
            """
        ),
        code(
            """
            cF (a * x ^ 3 + b * x ^ 2 + c * x + d) x
            """
        ),
        markdown(
            r"""
            ## Takeaway

            Cardano's formula becomes a short executable derivation when
            coefficient patterns, substitution, and root permutations are
            first-class operations. The three algebraic branches remain
            visible instead of being hidden behind a generic solver.
            """
        ),
    ]


def quartic_equation() -> list[dict]:
    return [
        markdown(
            r"""
            # Solving a Quartic Equation

            Ferrari's method first translates a quartic to

            $$
            y^4+py^2+qy+r=0.
            $$

            It then chooses a resolvent parameter $u$ so that the polynomial
            factors into two quadratics. The condition on $u$ is the cubic

            $$
            u(p+u)^2-4ru-q^2=0.
            $$
            """
        ),
        markdown(
            r"""
            ## Three structural cases

            A biquadratic ($q=0$) needs only two quadratic solves. A general
            depressed quartic uses the resolvent cubic. Finally,
            $x=y-b/4$ removes the cubic term from a monic quartic; a non-monic
            polynomial is normalized first.
            """
        ),
        code(
            """
            declare symbol x, y, u: MathValue

            def solveBiquadratic
              (p : MathValue)
              (q : MathValue)
              : (MathValue, MathValue, MathValue, MathValue) :=
              let (s1, s2) := qF' 1 p q
                  (r1, r2) := qF' 1 0 (- s1)
                  (r3, r4) := qF' 1 0 (- s2)
               in (r1, r2, r3, r4)
            """
        ),
        markdown(
            r"""
            ## Biquadratic shortcut

            For $x^4-5x^2+4=0$, the substitution $t=x^2$ yields
            $(t-1)(t-4)=0$.  Solving first for $t$ and then taking the two
            square roots of each value gives all four roots.
            """
        ),
        code(
            """
            solveBiquadratic (-5) 4
            """
        ),
        markdown(
            r"""
            ## Ferrari's general branch

            Consider the already-depressed polynomial

            $$
            y^4-15y^2-10y+24
              =(y+3)(y+2)(y-1)(y-4).
            $$

            Here $(p,q,r)=(-15,-10,24)$, so this is genuinely outside the
            biquadratic case.  Its resolvent has the convenient root $u=1$.
            """
        ),
        code(
            """
            def p : MathValue := -15
            def q : MathValue := -10
            def r : MathValue := 24
            def chosenU : MathValue := 1

            def resolvent (u : MathValue) : MathValue :=
              u * (p + u)^2 - 4 * r * u - q^2

            def factorPlus : MathValue :=
              y^2 + (p + chosenU) / 2
                + sqrt chosenU * (y - q / (2 * chosenU))

            def factorMinus : MathValue :=
              y^2 + (p + chosenU) / 2
                - sqrt chosenU * (y - q / (2 * chosenU))
            """
        ),
        code(
            """
            resolvent chosenU
            """
        ),
        code(
            """
            (factorPlus, factorMinus)
            """
        ),
        code(
            """
            (qF factorPlus y, qF factorMinus y)
            """
        ),
        markdown(
            r"""
            ## Why the factorization works

            Once a root $u$ of the resolvent is chosen, the depressed quartic is
            split into

            $$
            y^2+\frac{p+u}{2}
              \pm\sqrt{u}\left(y-\frac{q}{2u}\right)=0.
            $$

            The two calls to the quadratic solver return all four roots.
            """
        ),
        markdown(
            r"""
            ## Takeaway

            The two executable paths mirror Ferrari's proof: the biquadratic case
            reduces immediately to quadratic equations, while the nonzero-linear
            case uses one resolvent root to expose two quadratic factors.  Egison
            keeps the exact factorization and all four roots symbolic.
            """
        ),
    ]


def fifth_root_of_unity() -> list[dict]:
    return [
        markdown(
            r"""
            # The 5th Roots of Unity

            Let $\zeta=\exp(2\pi i/5)$. The primitive fifth roots satisfy

            $$
            \Phi_5(x)=x^4+x^3+x^2+x+1=0.
            $$

            In particular,

            $$
            \cos\frac{2\pi}{5}=\frac{\sqrt5-1}{4}.
            $$

            We recover this radical expression by organizing powers of
            $\zeta$ into orbits rather than asking a black-box polynomial
            solver for four roots at once.
            """
        ),
        markdown(
            r"""
            ## Pair conjugate powers

            Complex conjugation pairs $\zeta$ with $\zeta^4$ and $\zeta^2$
            with $\zeta^3$. Their symmetric sums are real. Adding the two
            pairs gives $-1$, the sum of all primitive fifth roots.
            """
        ),
        code(
            """
            def z : MathValue := rtu 5

            def a11 : MathValue := z ^ 1 + z ^ 4
            def a12 : MathValue := z ^ 2 + z ^ 3

            def b10 : MathValue := a11 + a12
            def b11 : MathValue := a11 - a12
            def b12 : MathValue := a12 - a11
            """
        ),
        code(
            """
            (b10, b11, b12)
            """
        ),
        markdown(
            r"""
            ## Invert the first two-point transform

            The sum is already $b_{10}=-1$. Squaring the difference removes
            its sign ambiguity; choosing a square-root branch and applying the
            inverse transform reconstructs the two real periods.
            """
        ),
        code(
            """
            def b10' : MathValue := b10
            def b11' : MathValue := sqrt (b11 ^ 2)

            def a11' : MathValue := (b10' + b11') / 2
            def a12' : MathValue := (b10' - b11') / 2
            """
        ),
        code(
            """
            (a11', a12')
            """
        ),
        markdown(
            r"""
            ## Recover the imaginary parts

            The antisymmetric pairs
            $\zeta-\zeta^{-1}$ and $\zeta^2-\zeta^{-2}$ carry the imaginary
            parts. A second two-point transform reduces them to square roots
            whose radicands depend only on the real periods above.
            """
        ),
        code(
            """
            def a21 : MathValue := z ^ 1 - z ^ 4
            def a22 : MathValue := z ^ 2 - z ^ 3

            def b20 : MathValue := a21 + a22
            def b21 : MathValue := a21 - a22
            def b22 : MathValue := a22 - a21

            def b20' : MathValue := sqrt ((-3) + 4 * a12')
            def b21' : MathValue := sqrt ((-3) + 4 * a11')

            def a21' : MathValue := (b20' + b21') / 2
            def a22' : MathValue := (b20' - b21') / 2

            def z1' : MathValue := (a11' + a21') / 2
            """
        ),
        code(
            """
            z1'
            """
        ),
        markdown(
            r"""
            ## Verify the radical relation

            Nested square roots introduce branch atoms that are algebraically
            related. The following ideal records their defining relations.
            Reducing $(z_1')^5-1$ modulo that ideal gives an exact symbolic
            check, rather than a floating-point approximation.
            """
        ),
        code(
            """
            def radicalRels : [MathValue] :=
              [ '((sqrt (5 + 2 * sqrt 5)) ^ 2 - 5 - 2 * sqrt 5)
              , '((sqrt (5 - 2 * sqrt 5)) ^ 2 - 5 + 2 * sqrt 5)
              , '((sqrt (5 + 2 * sqrt 5))
                    * (sqrt (5 - 2 * sqrt 5))
                    - sqrt 5)
              , '((sqrt 5) ^ 2 - 5)
              , '(i ^ 2 + 1) ]
            """
        ),
        code(
            """
            idealNF radicalRels (z1' ^ 5 - 1)
            """
        ),
        markdown(
            r"""
            ## Takeaway

            The familiar golden-ratio square root appears because the Galois
            group of $\Phi_5$ can be resolved by two successive two-point
            transforms. Egison keeps the orbit sums and the exact radical
            verification in the same symbolic calculation.
            """
        ),
    ]


def seventh_root_of_unity() -> list[dict]:
    return [
        markdown(
            r"""
            # The 7th Roots of Unity

            A primitive seventh root $\zeta$ satisfies

            $$
            \Phi_7(x)=x^6+x^5+x^4+x^3+x^2+x+1=0.
            $$

            The six primitive roots are permuted by
            $(\mathbb Z/7\mathbb Z)^\times$. We first quotient by complex
            conjugation, leaving three real periods, and then use a
            three-point Fourier transform over the cube roots of unity.
            """
        ),
        markdown(
            r"""
            ## Three conjugate periods

            Pairing exponents $k$ and $7-k$ gives
            $a_{11},a_{12},a_{13}$. Their sum is $-1$, because the sum of all
            nontrivial seventh roots is $-1$.
            """
        ),
        code(
            """
            def z : MathValue := rtu 7

            def a11 : MathValue := z ^ 1 + z ^ 6
            def a12 : MathValue := z ^ 2 + z ^ 5
            def a13 : MathValue := z ^ 3 + z ^ 4

            def b10 : MathValue := a11 + a12 + a13

            def cyclotomic7 : MathValue :=
              '((rtu 7)^6 + (rtu 7)^5 + (rtu 7)^4
                + (rtu 7)^3 + (rtu 7)^2 + rtu 7 + 1)

            def reduce7 (v : MathValue) : MathValue :=
              idealNFWith [w] [cyclotomic7] v

            def b10' : MathValue := reduce7 b10
            """
        ),
        code(
            """
            b10'
            """
        ),
        markdown(
            r"""
            ## Fourier resolvents

            With $\omega=(-1+i\sqrt3)/2$, the two nontrivial characters of the
            three-cycle produce two conjugate triples. Multiplying each triple
            removes the cyclic ambiguity. We reduce those products modulo
            $\Phi_7(\zeta)$, leaving expressions in $\omega$ alone, so one cube
            root recovers each Fourier component.
            """
        ),
        code(
            """
            def b11 : MathValue := a11 + w * a12 + w ^ 2 * a13
            def b12 : MathValue := a13 + w * a11 + w ^ 2 * a12
            def b13 : MathValue := a12 + w * a13 + w ^ 2 * a11

            def b14 : MathValue := a11 + w * a13 + w ^ 2 * a12
            def b15 : MathValue := a12 + w * a11 + w ^ 2 * a13
            def b16 : MathValue := a13 + w * a12 + w ^ 2 * a11

            def b11Cube : MathValue := reduce7 (b11 * b12 * b13)
            def b14Cube : MathValue := reduce7 (b14 * b15 * b16)
            """
        ),
        code(
            """
            (b11Cube, b14Cube, b11Cube * b14Cube)
            """
        ),
        markdown(
            r"""
            ## Invert the transform

            The two displayed radicands are conjugate and their product is
            $7^3$. We choose conjugate cube-root branches whose product is $7$
            and whose reconstructed real period is positive. Their inverse
            transform gives
            $a_{11}=\zeta+\zeta^{-1}=2\cos(2\pi/7)$.
            """
        ),
        code(
            """
            def b11' : MathValue := rt 3 b11Cube
            def b14' : MathValue := rt 3 b14Cube

            def a11' : MathValue := (b10' + b11' + b14') / 3
            """
        ),
        code(
            """
            a11' / 2
            """
        ),
        markdown(
            r"""
            ## Recover a root itself

            Once $a_{11}'=\zeta+\zeta^{-1}$ is known, $\zeta$ is a root of

            $$
            x^2-a_{11}'x+1=0.
            $$

            The selected radical branches determine which member of the
            conjugate pair appears first.
            """
        ),
        code(
            """
            def quadraticRoots7
              (a : MathValue)
              (b : MathValue)
              (c : MathValue)
              : (MathValue, MathValue) :=
              ( ((- b) + sqrt (b ^ 2 - 4 * a * c)) / (2 * a)
              , ((- b) - sqrt (b ^ 2 - 4 * a * c)) / (2 * a) )

            def z1' : MathValue := fst (quadraticRoots7 1 (- a11') 1)
            """
        ),
        code(
            """
            z1'
            """
        ),
        markdown(
            r"""
            Substitution into the final quadratic gives zero. This check is
            independent of how the nested square root is formatted.
            """
        ),
        code(
            """
            z1' ^ 2 - a11' * z1' + 1
            """
        ),
        markdown(
            r"""
            ## Takeaway

            A degree-six cyclotomic equation has been decomposed into one
            three-point transform, cube roots, and a final quadratic. The code
            follows the subgroup structure of the Galois group, making the
            origin of every radical visible.
            """
        ),
    ]


def ninth_root_of_unity() -> list[dict]:
    return [
        markdown(
            r"""
            # The 9th Roots of Unity

            The ninth-root equation factors as

            $$
            x^9-1=(x^3-1)(x^6+x^3+1).
            $$

            We solve the cyclotomic factor
            $\Phi_9(x)=x^6+x^3+1$. For a primitive root
            $\zeta=\exp(2\pi i/9)$, the result implies

            $$
            \cos\frac{2\pi}{9}
              =\frac{\sqrt[3]{\omega}+\sqrt[3]{\omega^2}}{2},
            \qquad \omega^3=1,\ \omega\ne1.
            $$
            """
        ),
        markdown(
            r"""
            ## Primitive conjugate pairs

            The primitive exponent classes modulo $9$ are
            $1,2,4,5,7,8$. Pairing inverses produces three real periods. Their
            sum is zero, in agreement with the vanishing sum of primitive
            ninth roots.
            """
        ),
        code(
            """
            def z : MathValue := rtu 9

            def a11 : MathValue := z ^ 1 + z ^ 8
            def a12 : MathValue := z ^ 2 + z ^ 7
            def a13 : MathValue := z ^ 4 + z ^ 5

            def b10 : MathValue := a11 + a12 + a13

            def cyclotomic9 : MathValue :=
              '((rtu 9)^6 + (rtu 9)^3 + 1)

            def reduce9 (v : MathValue) : MathValue :=
              idealNFWith [w] [cyclotomic9] v

            def b10' : MathValue := reduce9 b10
            """
        ),
        code(
            """
            b10'
            """
        ),
        markdown(
            r"""
            ## A modern three-point resolvent

            Multiplication of exponents by $2$ cycles the three periods. The
            following typed definitions are the two nontrivial Fourier
            resolvents for that cycle. This is a fresh translation into the
            current Egison syntax.
            """
        ),
        code(
            """
            def b11 : MathValue := a11 + w * a12 + w ^ 2 * a13
            def b12 : MathValue := a13 + w * a11 + w ^ 2 * a12
            def b13 : MathValue := a12 + w * a13 + w ^ 2 * a11

            def b14 : MathValue := a11 + w * a13 + w ^ 2 * a12
            def b15 : MathValue := a12 + w * a11 + w ^ 2 * a13
            def b16 : MathValue := a13 + w * a12 + w ^ 2 * a11

            def b11Cube : MathValue := reduce9 (b11 * b12 * b13)
            def b14Cube : MathValue := reduce9 (b14 * b15 * b16)
            """
        ),
        code(
            """
            (b11Cube, b14Cube, b11Cube * b14Cube)
            """
        ),
        markdown(
            r"""
            ## Choose cube-root branches

            The products simplify to $27\omega$ and $27\omega^2$, and their
            product is $9^3$. We choose conjugate cube-root branches whose
            product is $9$ and for which the reconstructed period satisfies
            $a_{11}'>1$. This selects the period $2\cos(2\pi/9)$ uniquely.
            Taking those roots and applying the inverse Fourier transform gives

            $$
            a_{11}'=\sqrt[3]{\omega}+\sqrt[3]{\omega^2}
                   =2\cos(2\pi/9).
            $$
            """
        ),
        code(
            """
            def b11' : MathValue := rt 3 b11Cube
            def b14' : MathValue := rt 3 b14Cube

            def a11' : MathValue := (b10' + b11' + b14') / 3
            """
        ),
        code(
            """
            a11' / 2
            """
        ),
        markdown(
            r"""
            ## Recover a primitive ninth root

            As before, $\zeta+\zeta^{-1}=a_{11}'$ turns the last step into the
            quadratic $x^2-a_{11}'x+1=0$.
            """
        ),
        code(
            """
            def quadraticRoots9
              (a : MathValue)
              (b : MathValue)
              (c : MathValue)
              : (MathValue, MathValue) :=
              ( ((- b) + sqrt (b ^ 2 - 4 * a * c)) / (2 * a)
              , ((- b) - sqrt (b ^ 2 - 4 * a * c)) / (2 * a) )

            def z1' : MathValue := fst (quadraticRoots9 1 (- a11') 1)
            """
        ),
        code(
            """
            z1'
            """
        ),
        markdown(
            r"""
            The constructed radical satisfies its final quadratic exactly.
            """
        ),
        code(
            """
            z1' ^ 2 - a11' * z1' + 1
            """
        ),
        markdown(
            r"""
            ## The cyclotomic check

            The exact root-of-unity object confirms both the ninth-power
            relation and its primitive cyclotomic factor.
            """
        ),
        code(
            """
            (z ^ 9, reduce9 (z ^ 6 + z ^ 3 + 1))
            """
        ),
        markdown(
            r"""
            ## Takeaway

            The factorization of $x^9-1$ isolates a degree-six problem, and the
            cyclic action on primitive exponents reduces it to cube roots plus
            one quadratic. The notebook uses only the current typed Egison
            surface syntax while preserving the original Galois-theoretic idea.
            """
        ),
    ]


def seventeenth_root_of_unity() -> list[dict]:
    return [
        markdown(
            r"""
            # The 17th Roots of Unity

            The regular $17$-gon is constructible because
            $17=2^{2^2}+1$ is a Fermat prime. Algebraically, the Galois group
            of

            $$
            \Phi_{17}(x)=x^{16}+x^{15}+\cdots+x+1
            $$

            has order $16$. A chain of index-two subgroups therefore resolves
            a primitive root using square roots alone.
            """
        ),
        markdown(
            r"""
            ## Eight real Gaussian periods

            Let $\zeta=\exp(2\pi i/17)$. Pairing each power with its inverse
            gives eight real quantities

            $$
            a_k=\zeta^k+\zeta^{-k}=2\cos(2\pi k/17).
            $$
            """
        ),
        code(
            """
            def z : MathValue := rtu 17

            def a1 : MathValue := z ^ 1 + z ^ 16
            def a2 : MathValue := z ^ 2 + z ^ 15
            def a3 : MathValue := z ^ 3 + z ^ 14
            def a4 : MathValue := z ^ 4 + z ^ 13
            def a5 : MathValue := z ^ 5 + z ^ 12
            def a6 : MathValue := z ^ 6 + z ^ 11
            def a7 : MathValue := z ^ 7 + z ^ 10
            def a8 : MathValue := z ^ 8 + z ^ 9
            """
        ),
        code(
            """
            a1 + a2 + a3 + a4 + a5 + a6 + a7 + a8
            """
        ),
        markdown(
            r"""
            ## Successive two-point transforms

            The multiplicative group modulo $17$ is cyclic. The definitions
            below follow its subgroup chain, repeatedly recording sums and
            differences. At the top level $d_{10}$ is the sum of all sixteen
            nontrivial roots and hence equals $-1$.
            """
        ),
        code(
            """
            def b11 : MathValue := a1 + a4
            def b12 : MathValue := a1 - a4
            def b21 : MathValue := a2 + a8
            def b22 : MathValue := a2 - a8
            def b31 : MathValue := a3 + a5
            def b32 : MathValue := a3 - a5
            def b41 : MathValue := a6 + a7
            def b42 : MathValue := a6 - a7

            def c11 : MathValue := b11 + b21
            def c12 : MathValue := b11 - b21
            def c21 : MathValue := b31 + b41
            def c22 : MathValue := b31 - b41

            def d10 : MathValue := c11 + c21
            def d11 : MathValue := c11 - c21
            def d12 : MathValue := c21 - c11
            """
        ),
        code(
            """
            (d10, d11, d12)
            """
        ),
        markdown(
            r"""
            ## Invert the subgroup chain

            Each difference has a square that can be expressed using quantities
            already known one level higher. Choosing compatible square-root
            branches and repeatedly applying

            $$
            u=\frac{(u+v)+(u-v)}{2}
            $$

            reconstructs the first period $a_1$.
            """
        ),
        code(
            """
            def d10' : MathValue := -1
            def d11' : MathValue := sqrt 17

            def c11' : MathValue := (d10' + d11') / 2
            def c21' : MathValue := (d10' - d11') / 2
            def c12' : MathValue := sqrt (8 + (- c11'))
            def c22' : MathValue := sqrt (8 + (- c21'))

            def b11' : MathValue := (c11' + c12') / 2
            def b21' : MathValue := (c11' - c12') / 2
            def b31' : MathValue := (c21' + c22') / 2
            def b41' : MathValue := (c21' - c22') / 2

            def b12' : MathValue := sqrt (4 + b21' + (-2) * b31')
            def b22' : MathValue := sqrt (4 + b21' + (-2) * b41')
            def b32' : MathValue := sqrt (4 + b41' + (-2) * b21')
            def b42' : MathValue := sqrt (4 + b31' + (-2) * b21')

            def a1' : MathValue := (b11' + b12') / 2
            """
        ),
        markdown(
            r"""
            ## Gauss's cosine formula

            Since $a_1'=2\cos(2\pi/17)$, dividing by two displays the classical
            nested-square-root construction of the regular $17$-gon:

            $$
            \cos\frac{2\pi}{17}
            =\frac1{16}\left(
              -1+\sqrt{17}+\sqrt{34-2\sqrt{17}}
              +2\sqrt{17+3\sqrt{17}-\sqrt{34-2\sqrt{17}}
                -2\sqrt{34+2\sqrt{17}}}
            \right).
            $$
            """
        ),
        code(
            """
            a1' / 2
            """
        ),
        markdown(
            r"""
            ## Root-of-unity check

            Egison's exact root-of-unity value retains the defining relation
            without numerical rounding.
            """
        ),
        code(
            """
            z ^ 17
            """
        ),
        markdown(
            r"""
            ## Takeaway

            The nested radicals are a direct trace of four successive
            index-two reductions in the Galois group. The computation explains
            not only the value of the cosine but also why straightedge-and-
            compass construction is possible.
            """
        ),
    ]


def tribonacci() -> list[dict]:
    return [
        markdown(
            r"""
            # Tribonacci Numbers by Matrix Exponentiation

            The Tribonacci sequence used here is

            $$
            T_0=0,\quad T_1=0,\quad T_2=1,\qquad
            T_{n+3}=T_{n+2}+T_{n+1}+T_n.
            $$

            A companion matrix turns this recurrence into repeated linear
            algebra, which makes fast exponentiation available.
            """
        ),
        markdown(
            r"""
            ## Build the transition matrix by pattern matching

            The first row sums the three current state entries. The
            subdiagonal shifts the older values down one position:

            $$
            A=
            \begin{pmatrix}
            1&1&1\\
            1&0&0\\
            0&1&0
            \end{pmatrix}.
            $$

            The generator describes those two structural patterns rather than
            listing nine unrelated entries.
            """
        ),
        code(
            """
            def m : Integer := 3

            def A : Matrix Integer :=
              generateTensor
                (\\match as list integer with
                  | [#1, _] -> 1
                  | [$x, #(x - 1)] -> 1
                  | _ -> 0)
                [m, m]
            """
        ),
        code(
            """
            A
            """
        ),
        markdown(
            r"""
            ## Initial state

            The vector $B=(1,0,0)^\mathsf T$ stores
            $(T_2,T_1,T_0)^\mathsf T$.
            """
        ),
        code(
            """
            def B : Vector Integer :=
              generateTensor
                (\\[x] -> if x = 1 then 1 else 0)
                [m]

            def tribonacciState (n : Integer) : Vector Integer :=
              MV.* (M.power A n) B
            """
        ),
        code(
            """
            B
            """
        ),
        markdown(
            r"""
            ## Advance the recurrence

            For every $n\ge0$,

            $$
            A^nB=(T_{n+2},T_{n+1},T_n)^\mathsf T.
            $$

            The first few full states make both the recurrence and the indexing
            convention visible.
            """
        ),
        code(
            """
            tribonacciState 1
            """
        ),
        code(
            """
            tribonacciState 3
            """
        ),
        code(
            """
            tribonacciState 5
            """
        ),
        markdown(
            r"""
            ## Jump directly to a large index

            Matrix exponentiation uses repeated squaring, so computing
            $A^{100}B$ does not require one hundred explicit recurrence steps.
            """
        ),
        code(
            """
            tribonacciState 100
            """
        ),
        markdown(
            r"""
            ## Takeaway

            Pattern matching gives a compact structural definition of the
            companion matrix, while tensor contraction performs the
            matrix-vector product. The first component of the final vector is
            $T_{102}$ under the stated indexing convention.
            """
        ),
    ]


def eulers_totient_function() -> list[dict]:
    return [
        markdown(
            r"""
            # Euler's Totient Function

            Euler's totient $\varphi(n)$ counts integers in
            $\{1,\ldots,n\}$ that are coprime to $n$. If the distinct prime
            divisors of $n$ are $p_1,\ldots,p_k$, then

            $$
            \varphi(n)
              =n\prod_{j=1}^k\left(1-\frac1{p_j}\right).
            $$

            The product formula makes prime factorization the natural
            computational route.
            """
        ),
        markdown(
            r"""
            ## A direct typed definition

            Prime factorization may contain repeated primes, so unique removes
            duplicates before the product is taken. Rational arithmetic keeps
            every intermediate factor exact even though the final result is an
            integer.
            """
        ),
        code(
            """
            def φ (n : Integer) : Rational :=
              n * product (map (\\p -> 1 - 1 / p) (unique (pF n)))
            """
        ),
        markdown(
            r"""
            ## Inspect one factorization

            Since $36=2^2\,3^2$, only the distinct primes $2$ and $3$ enter:

            $$
            \varphi(36)=36(1-1/2)(1-1/3)=12.
            $$
            """
        ),
        code(
            """
            (pF 36, unique (pF 36), φ 36)
            """
        ),
        markdown(
            r"""
            ## The first twenty values

            Displaying each $n$, its totient, and its complete prime
            factorization makes the jumps at primes and prime powers easy to
            compare.
            """
        ),
        code(
            """
            map (\\n -> (n, φ n, pF n)) (take 20 nats)
            """
        ),
        markdown(
            r"""
            ## A divisor-sum identity

            Every positive integer satisfies

            $$
            \sum_{d\mid n}\varphi(d)=n.
            $$

            We can express the divisor condition with an ordinary filter and
            verify the identity on the same example.
            """
        ),
        code(
            """
            def divisorsOf (n : Integer) : [Integer] :=
              filter (\\d -> divisor n d) [1..n]

            def totientDivisorSum (n : Integer) : Rational :=
              sum (map φ (divisorsOf n))
            """
        ),
        code(
            """
            (divisorsOf 36, totientDivisorSum 36)
            """
        ),
        markdown(
            r"""
            ## Takeaway

            Euler's product formula becomes a one-line exact definition when
            factorization, uniqueness, mapping, and products compose directly.
            The divisor-sum check shows how the same function participates in a
            deeper arithmetic identity.
            """
        ),
    ]


def gaussian_primes() -> list[dict]:
    return [
        markdown(
            r"""
            # Gaussian Primes

            The Gaussian integers are

            $$
            \mathbb Z[i]=\{a+bi\mid a,b\in\mathbb Z\}.
            $$

            Their multiplicative norm is

            $$
            N(a+bi)=(a+bi)(a-bi)=a^2+b^2.
            $$

            Away from the coordinate axes, a Gaussian integer is prime exactly
            when its integer norm is prime.
            """
        ),
        markdown(
            r"""
            ## Enumerate a finite lattice patch

            Egison's set matcher chooses unordered pairs from
            $\{1,\ldots,10\}$. This covers one open quadrant without listing
            symmetric associates produced by signs, conjugation, or
            multiplication by the units $\{\pm1,\pm i\}$.
            """
        ),
        code(
            """
            def gaussianPoints : [(Integer, Integer)] :=
              matchAll take 10 nats as set integer with
                | $x :: $y :: _ -> (x, y)

            def gaussianInteger (x : Integer) (y : Integer) : MathValue :=
              x + y * i

            def gaussianNorm (x : Integer) (y : Integer) : Integer :=
              x ^ 2 + y ^ 2

            def gaussianNorms : [(MathValue, Integer)] :=
              map
                (\\(x, y) -> (gaussianInteger x y, gaussianNorm x y))
                gaussianPoints
            """
        ),
        markdown(
            r"""
            ## Norms are ordinary integers

            The first entries show both the algebraic integer and its exact
            norm. For example, $N(1+i)=2$, while $N(2+2i)=8$.
            """
        ),
        code(
            """
            take 10 gaussianNorms
            """
        ),
        markdown(
            r"""
            ## Filter by prime norm

            Because both coordinates in this patch are nonzero, testing the
            integer norm is sufficient. Axis primes require the complementary
            rule that an ordinary prime $p$ remains Gaussian-prime precisely
            when $p\equiv3\pmod4$.
            """
        ),
        code(
            """
            def gaussianPrimes : [(MathValue, Integer)] :=
              filter (\\(_, n) -> isPrime n) gaussianNorms
            """
        ),
        code(
            """
            take 20 gaussianPrimes
            """
        ),
        markdown(
            r"""
            ## Multiplicativity in one line

            The rational prime $2$ is not prime in $\mathbb Z[i]$:

            $$
            2=(1+i)(1-i).
            $$

            The same expression also exhibits the norm of $1+i$.
            """
        ),
        code(
            """
            ((1 + i) * (1 - i), gaussianNorm 1 1)
            """
        ),
        markdown(
            r"""
            ## Takeaway

            A two-dimensional primality question has been reduced to an
            ordinary integer test through the multiplicative norm. Egison's
            pattern matching handles the lattice enumeration, while exact
            symbolic arithmetic keeps each Gaussian integer readable.
            """
        ),
    ]


def eisenstein_primes() -> list[dict]:
    return [
        markdown(
            r"""
            # Eisenstein Primes

            Let

            $$
            \omega=\frac{-1+i\sqrt3}{2},\qquad
            \omega^2+\omega+1=0.
            $$

            The Eisenstein integers are $\mathbb Z[\omega]$. Their norm is

            $$
            N(a+b\omega)
              =(a+b\omega)(a+b\omega^2)
              =a^2-ab+b^2.
            $$
            """
        ),
        markdown(
            r"""
            ## Enumerate one sector of the lattice

            We again use unordered positive coordinate pairs from a finite
            patch. The six units and conjugation generate the symmetric copies
            in the remaining sectors of the triangular Eisenstein lattice.
            """
        ),
        code(
            """
            def eisensteinPoints : [(Integer, Integer)] :=
              matchAll take 10 nats as set integer with
                | $x :: $y :: _ -> (x, y)

            def eisensteinInteger (x : Integer) (y : Integer) : MathValue :=
              x + y * w

            def eisensteinNorm (x : Integer) (y : Integer) : Integer :=
              x ^ 2 - x * y + y ^ 2

            def eisensteinNorms : [(MathValue, Integer)] :=
              map
                (\\(x, y) -> (eisensteinInteger x y, eisensteinNorm x y))
                eisensteinPoints
            """
        ),
        markdown(
            r"""
            ## Check the defining relation and norm

            The first component below is zero by
            $\omega^2+\omega+1=0$. The other entries show, for example, that
            $1+2\omega$ has norm $3$.
            """
        ),
        code(
            """
            (w ^ 2 + w + 1, eisensteinNorm 1 2, take 10 eisensteinNorms)
            """
        ),
        markdown(
            r"""
            ## Filter by prime norm

            In the interior of this positive-coordinate sector, a prime integer
            norm certifies an Eisenstein prime. The norm-one element
            $1+\omega$ is a unit and is automatically excluded.
            """
        ),
        code(
            """
            def eisensteinPrimes : [(MathValue, Integer)] :=
              filter (\\(_, n) -> isPrime n) eisensteinNorms
            """
        ),
        code(
            """
            take 24 eisensteinPrimes
            """
        ),
        markdown(
            r"""
            ## Rational primes behave differently here

            An ordinary prime $p\ne3$ splits in $\mathbb Z[\omega]$ when
            $p\equiv1\pmod3$ and remains prime when $p\equiv2\pmod3$.
            The ramified prime is

            $$
            3=-\omega^2(1-\omega)^2.
            $$

            Its basic factor has norm $3$.
            """
        ),
        code(
            """
            ((1 - w) * (1 - w ^ 2), eisensteinNorm 1 (-1))
            """
        ),
        markdown(
            r"""
            ## Takeaway

            Replacing the square lattice by a triangular one changes the norm
            from $a^2+b^2$ to $a^2-ab+b^2$, but the computational idea is the
            same: enumerate algebraic integers structurally and transfer
            primality to exact arithmetic in $\mathbb Z$.
            """
        ),
    ]


NOTEBOOKS = {
    "quadratic-equation": quadratic_equation,
    "cubic-equation": cubic_equation,
    "quartic-equation": quartic_equation,
    "5th-root-of-unity": fifth_root_of_unity,
    "7th-root-of-unity": seventh_root_of_unity,
    "9th-root-of-unity": ninth_root_of_unity,
    "17th-root-of-unity": seventeenth_root_of_unity,
    "tribonacci": tribonacci,
    "eulers-totient-function": eulers_totient_function,
    "gaussian-primes": gaussian_primes,
    "eisenstein-primes": eisenstein_primes,
}


def main() -> None:
    for slug, build_cells in NOTEBOOKS.items():
        print(write_notebook(slug, build_cells()))


if __name__ == "__main__":
    main()
