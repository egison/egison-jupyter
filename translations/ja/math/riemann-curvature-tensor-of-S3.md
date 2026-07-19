<!--
notebook: riemann-curvature-tensor-of-S3
source-markdown-sha256: 2464c00065ab35eb69367fcb8adb24f76a0ac2e53509cb1c70b928dbbad56d5d
-->

<!-- cell: 869503fe -->
# 3次元超球面 $S^3$ のリーマン曲率テンソル

半径 $r$ の丸い3次元超球面は、一定の断面曲率 $1/r^2$ をもちます。
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

<!-- cell: 06b4bec5 -->
## 超球面座標チャート

座標を $x=(\theta, \phi, \psi)$ とします。標準埋め込み
$X:S^3\hookrightarrow\mathbb{R}^4$ は、
$X_1=r\cos \theta$、$X_2=r\sin \theta\cos \phi$、……のように、
正弦を順次掛け合わせる形で構成されます。これにより
$X\mathbin{\cdot}X=r^2$ が明らかになります。

このチャートは通常の座標極を含みません。そこで現れる特異性は
超球面座標に由来するものであり、丸い超球面の幾何そのものの
特異性ではありません。

<!-- cell: 76ea3fb4 -->
## 計量と逆計量

埋め込みを微分すると、直交する座標基底が得られます。その線素は

$$
ds^2=r^2\left(d\theta^2 + \sin^2 \theta d\phi^2 + \sin^2 \theta \sin^2 \phi d\psi^2\right).
$$

Egisonは埋め込みを微分して座標接ベクトルを求め、それらの内積として
各成分 $g_{ij}=\partial_iX\mathbin{\cdot}\partial_jX$ を構成します。
逆計量は、この誘導計量から計算します。

<!-- cell: 9d09a29e -->
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

<!-- cell: 82554fac -->
## リーマンテンソル

以下の定義は、冒頭で示した符号規約をそのまま転記したものです。
2つの出力セルは、テンソルの最初の2つのスロットを入れ替えながら、
同じ座標2平面上の成分を取り出しています。両者に異なる座標因子が
現れるのは、座標基底が正規直交基底ではないことから予想される通りです。

<!-- cell: e832d1aa -->
## リッチ曲率とスカラー曲率

リーマンテンソルの第1添字と第3添字を縮約すると

$$
\operatorname{Ric}_{ij}=R^m{}_{imj},
\qquad
\mathcal{R}=g^{ij}\operatorname{Ric}_{ij}.
$$

丸い $S^3$ に対して、座標に依存しない形では

$$
\operatorname{Ric}=\frac{2}{r^2}g,
\qquad
\mathcal{R}=\frac{6}{r^2}.
$$

<!-- cell: 0b3e8898 -->
## 結果の解釈

取り出した各成分は座標に依存しますが、それらを縮約すると不変な主張が
得られます。すなわち、すべての接2平面の断面曲率は $1/r^2$、計量は
アインシュタイン計量、スカラー曲率は $6/r^2$ です。
$\sin \theta$ のような因子がチャートの極で消えるのは、そこで座標枠が
退化するためです。曲率そのものは滑らかなままです。
