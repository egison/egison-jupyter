<!--
notebook: emr-thurston-wcs-invariant
source-markdown-sha256: 0e18c99c0d7a34d972eef98486638da9d7c8ea65bbfdbdcfae9ccb1a3f40cf3d
-->

<!-- cell: 3ab7f4fc -->
# Thurston例におけるWodzicki–Chern–Simons不変量

このNotebookは、論文 *Diffeomorphism Groups of Circle Bundles over Integral
Symplectic Manifolds* の第4節にある数式処理計算を再現します。計量、曲率、
持ち上げた曲率テンソルを構成し、Wodzicki–Chern–Simons積分核をコンパクトな
有理式へ簡約します。

研究で使用した元のプログラムは
[EMR-Paper-Computation](https://github.com/egisatoshi/EMR-Paper-Computation)
で保守されています。

<!-- cell: a1b172c6 -->
## Thurston計量

$\beta=1+\theta_2-\theta_2^2$ とおきます。以下の計量と逆計量は、座標枠
$(\theta_1,\theta_2,\theta_3,\theta_4)$ で表されています。繰り返し現れる
2つの多項式をquoteすることで、テンソル計算の中間式をコンパクトに保ちます。

<!-- cell: 54a496ff -->
## Levi-Civita接続と曲率

Egisonの記号的なテンソル添字を使って、通常の公式をそのまま記述します。

$$
\Gamma^c{}_{ab}=\frac12g^{ce}
  (\partial_ag_{be}+\partial_bg_{ae}-\partial_eg_{ab}),
$$

続いて $R_{ijk}{}^l$ を計算します。上付きと下付きで繰り返す添字は `.` により
縮約されます。

<!-- cell: cae61ba3 -->
## 複素構造と持ち上げた曲率

複素構造 $J$ とその共変微分から、円周束上の曲率 $R'$ が定まります。
第1座標はファイバー方向で、残りの4座標はThurston底空間に属します。

<!-- cell: da3db121 -->
## Wodzicki–Chern–Simons縮約

交代縮約には $R'$ が3回現れます。生の結果にはquoteされた原子 $\beta$ の
負の冪が含まれます。$16\beta^8$ を掛けてLaurent分母を払い、quoteの定義関係に
対するGröbner基底を使って標準的な多項式正規形を求めたあと、分母を戻します。

<!-- cell: b369a39c -->
## 結果

Egisonは完全な縮約を次の形まで簡約します。

$$
S=192p^6\kappa-\frac{40p^4\kappa}{\beta^2}
  -\frac{25p^2\kappa}{16\beta^4}
 =\frac{p^2\kappa(-25-640p^2\beta^2+3072p^4\beta^4)}
        {16\beta^4}.
$$

以前は外部の数式処理システムで簡約していた式を、現在はEgisonだけで計算し、
正規化できます。
