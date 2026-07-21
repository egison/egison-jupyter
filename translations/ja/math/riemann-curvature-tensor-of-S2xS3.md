<!--
notebook: riemann-curvature-tensor-of-S2xS3
source-markdown-sha256: 4ae81cf129d5a9d65bb57ab5a5e087c1826399fa230d9c1a3b84227bd7a840f7
-->

<!-- cell: 597d65fd -->
# $S^2\times S^3$ 上のアインシュタイン計量

「$S^2\times S^3$ のリーマン曲率テンソル」という名前で公開されてきた
Egisonのデモは、2つの丸い計量の単純なブロック直積ではなく、非対角な
5次元計量を扱います。その目標は、次のアインシュタイン条件を確かめる
ことです。

$$
\operatorname{Ric}_{ij}=4g_{ij},\qquad \mathcal R=20.
$$

このNotebookでは、その計量を引き継ぎつつ、記号計算に必要な計算量を
明示します。計量や接続の小さな成分は対話的な出力に適していますが、
アインシュタイン条件の残差全体は、必要に応じて明示的に評価できるよう
定義だけを用意します。

<!-- cell: 3b2a5c7e -->
## 座標と略記

座標の順序を $x=(\phi,\theta,\psi,y,\alpha)$ とし、次の略記を導入します。

$$
p=1-y,\quad u=a-y^2,\quad
v=a-3y^2+2y^3,\quad q=a-2y+y^2.
$$

これらの因子によって、元の計量に繰り返し現れる構造が見やすくなり、
座標領域の制約（$p u v\ne0$）も明確になります。

<!-- cell: 40c363a8 -->
## 局所フレームと誘導計量

$f=q/(6u)$とおきます。計量は、正規直交フレームを用いて次のように
分解できます。

$$
\begin{split}
ds^2={}&\frac p6(d\theta^2+\sin^2\theta\,d\phi^2)
  +\frac{p}{2v}dy^2
  +\frac{v}{9u}(d\psi-\cos\theta\,d\phi)^2\\
  &+\frac{2u}{p}
    \bigl(d\alpha+f(d\psi-\cos\theta\,d\phi)\bigr)^2.
\end{split}
$$

下の`e_i_j`の各行は、座標接ベクトル$e_i$をこの正規直交フレームで
表したものです。丸い球面のNotebookと同じように、Egisonは接ベクトルの
内積$g_{ij}=e_i\mathbin{\cdot}e_j$からすべての計量成分を構成します。
$(1,3,5)$ブロックの結合は、$d\psi-\cos\theta\,d\phi$が2か所に現れる
ことから生成されます。

<!-- cell: 2a675a89 -->
## 接続と曲率の計算手順

第一種クリストッフェル記号には、上で示した計量の微分だけが必要です。
添字を上げる段階で、結合したブロックの逆行列が現れます。それでも、
リーマンテンソルとリッチテンソルの定義は低次元の例と同じです。

$$
R^i{}_{jkl}=\partial_k\Gamma^i{}_{jl}-\partial_l\Gamma^i{}_{jk}
  +\Gamma^m{}_{jl}\Gamma^i{}_{mk}-\Gamma^m{}_{jk}\Gamma^i{}_{ml},
\qquad
\operatorname{Ric}_{ij}=R^m{}_{imj}.
$$

<!-- cell: 6ac949ef -->
## 結果の解釈と評価方針

例として取り出した2つの第一種クリストッフェル記号は、単純な成分
$g_{22}=p/6$ から得られ、期待される対称性
$\Gamma_{ijk}=\Gamma_{ikj}$ を示します。完全な検証を表すのが
`einsteinResidual_#_#` です。数学的にはこれは零行列となるため、
スカラー曲率は $5\cdot4=20$ です。

残差の25成分をすべて展開すると、結合ブロックの逆行列と多数の有理式の
簡約が必要になります。そのため、意図的に自動実行される出力セルには
していません。この恒等式を対話的に調べるときは、
`einsteinResidual_2_2` のような個々の成分を評価してください。
