<!--
notebook: riemann-curvature-tensor-of-S7
source-markdown-sha256: 4a114e5cbfe86b720f3fa3a3e81123752dc11135b28064ab8dfd0af54277e423
-->

<!-- cell: bf752426 -->
# 7次元超球面 $S^7$ のリーマン曲率テンソル

半径 $r$ の丸い7次元超球面は、一定の断面曲率 $1/r^2$ をもちます。
このNotebookでは、添字付きのEgison記法を使って、その計量、
レヴィ・チヴィタ接続、リーマンテンソル、リッチテンソル、スカラー曲率を
順に構成します。

ここでは次の符号規約を採用します。

$$
R^i{}_{jkl}
  = \partial_k\Gamma^i{}_{jl}
  - \partial_l\Gamma^i{}_{jk}
  + \Gamma^m{}_{jl}\Gamma^i{}_{mk}
  - \Gamma^m{}_{jk}\Gamma^i{}_{ml}.
$$

<!-- cell: e69d2760 -->
## 超球面座標チャート

座標を $x=(\alpha, \beta, \gamma, \delta, \xi, \zeta, \eta)$ とします。
標準埋め込み $X:S^7\hookrightarrow\mathbb{R}^8$ は、
$X_1=r\cos \alpha$、$X_2=r\sin \alpha\cos \beta$、……のように、
正弦を順次掛け合わせる形で構成されます。これにより
$X\mathbin{\cdot}X=r^2$ が明らかになります。

このチャートは通常の座標極を含みません。そこで現れる特異性は
超球面座標に由来するものであり、丸い超球面の幾何そのものの
特異性ではありません。

<!-- cell: 2d70bfb3 -->
## 計量と逆計量

埋め込みを微分すると、直交する座標基底が得られます。その線素は

$$
ds^2=r^2\left(d\alpha^2 + \sin^2 \alpha d\beta^2 + \sin^2 \alpha \sin^2 \beta d\gamma^2 + \sin^2 \alpha \sin^2 \beta \sin^2 \gamma d\delta^2 + \sin^2 \alpha \sin^2 \beta \sin^2 \gamma \sin^2 \delta d\xi^2 + \sin^2 \alpha \sin^2 \beta \sin^2 \gamma \sin^2 \delta \sin^2 \xi d\zeta^2 + \sin^2 \alpha \sin^2 \beta \sin^2 \gamma \sin^2 \delta \sin^2 \xi \sin^2 \zeta d\eta^2\right).
$$

この対角形式をここでは明示的に入力します。これによりNotebookの計算を
高速に保ちながら、
$g_{ij}=\partial_iX\mathbin{\cdot}\partial_jX$ から導かれるものと
同じ計量を使えます。

<!-- cell: c1ba9dd2 -->
## レヴィ・チヴィタ接続

第一種および第二種クリストッフェル記号は

$$
\Gamma_{ijk}=\frac12
(\partial_jg_{ik}+\partial_kg_{ij}-\partial_ig_{jk}),
\qquad
\Gamma^i{}_{jk}=g^{im}\Gamma_{mjk}.
$$

重複する記号添字は `.` によって縮約されます。`withSymbols` ブロックは、
ダミー添字のスコープを定義の内部に限定します。

<!-- cell: 217655ad -->
## リーマンテンソル

以下の定義は、冒頭で示した符号規約をそのまま転記したものです。
2つの出力セルは、テンソルの最初の2つのスロットを入れ替えながら、
同じ座標2平面上の成分を取り出しています。両者に異なる座標因子が
現れるのは、座標基底が正規直交基底ではないことから予想される通りです。

<!-- cell: bb792202 -->
## リッチ曲率とスカラー曲率

リーマンテンソルの第1添字と第3添字を縮約すると

$$
\operatorname{Ric}_{ij}=R^m{}_{imj},
\qquad
\mathcal{R}=g^{ij}\operatorname{Ric}_{ij}.
$$

丸い $S^7$ に対して、座標に依存しない形では

$$
\operatorname{Ric}=\frac{6}{r^2}g,
\qquad
\mathcal{R}=\frac{42}{r^2}.
$$

<!-- cell: 9ae135a3 -->
## 結果の解釈

取り出した各成分は座標に依存しますが、それらを縮約すると不変な主張が
得られます。すなわち、すべての接2平面の断面曲率は $1/r^2$、計量は
アインシュタイン計量、スカラー曲率は $42/r^2$ です。
$\sin \alpha$ のような因子がチャートの極で消えるのは、そこで座標枠が
退化するためです。曲率そのものは滑らかなままです。リッチ曲率と
スカラー曲率の定義は含まれていますが、それらの完全な縮約は意図的に
出力セルにしていません。選んだリーマンテンソルの成分だけで、巨大な
記号式展開を実行せずに一定曲率のパターンを確認できます。
