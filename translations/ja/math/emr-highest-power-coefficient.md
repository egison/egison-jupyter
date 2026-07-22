<!--
notebook: emr-highest-power-coefficient
source-markdown-sha256: ef7fb65173e3f3856f70420b525bc95448ac526d016fd29241de9fdebfb466a7
-->

<!-- cell: 9ef0376e -->
# EMR曲率公式における最高次係数

このNotebookは、論文 *Diffeomorphism Groups of Circle Bundles over Integral
Symplectic Manifolds* の定理3.4で用いられる有限次元計算を再現します。
すべての置換について符号付き和を取り、標準複素構造のコピーを縮約します。

研究で使用した完全なコードは
[EMR-Paper-Computation](https://github.com/egisatoshi/EMR-Paper-Computation)
で公開されています。

<!-- cell: d3711f1e -->
## 標準複素構造

$2k$ 次元実ベクトル空間上で

$$
J=\begin{pmatrix}0&I_k\\-I_k&0\end{pmatrix}.
$$

とします。このNotebookでは、対話的にすばやく計算できるよう $k=2$ を使います。
最後の節では、まったく同じ定義を使ったより大きな計算結果も示します。

<!-- cell: 277c0f2d -->
## 交代積

$S_k$ を次の積の符号付き和とします。

$$
S_k=\sum_{\sigma\in S_{2k}}\operatorname{sgn}(\sigma)
    \prod_{i=1}^{k}J_{\sigma(2i-1),\sigma(2i)}.
$$

`evenAndOddPermutations` は偶置換と奇置換を別々に生成します。

<!-- cell: 40b251a9 -->
## 曲率の係数

束のパラメータ $p$ の最高次項は、次のテンソルから構成されます。

$$
T_{abc}{}^d=-J_{bc}J_a{}^d+J_{ac}J_b{}^d
             +2J_{ab}J_c{}^d.
$$

添字 $a_0,\ldots,a_{k-1}$ は巡回的な鎖を作ります。テンソル積に続く `.` が
この鎖を縮約し、外側の畳み込みが偶置換と奇置換からの寄与を加算します。

<!-- cell: ed1338ff -->
## より高い次元

同じプログラムから次の結果が得られます。

$$
\begin{array}{c|rr}
k&S_k&S'_k\\ \hline
2&-8&192\\
3&-48&0\\
4&384&61440
\end{array}
$$

Egison 5.1.0で $k=4$ の完全な計算には約25分かかります。対話的なNotebookを
$k=2$ にしておくことで、各セルをすばやく再実行できます。最初の定義を
`def k := 4` に変えるだけで、他のコードを変更せずに定理3.4の完全な計算を
実行できます。
