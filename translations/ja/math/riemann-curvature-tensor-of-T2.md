<!--
notebook: riemann-curvature-tensor-of-T2
source-markdown-sha256: 3ec329e0dffc53f8edc7c26265438e0bb19da74a7c7b80a88b4d599d091cc4fb
-->

<!-- cell: 71d40661 -->
# 埋め込みトーラス$T^2$のリーマン曲率テンソル

管半径$a$、大半径$b$の環状トーラスを次のように埋め込みます。

$$
X(\theta,\phi)=\bigl((b+a\cos\theta)\cos\phi,
(b+a\cos\theta)\sin\phi,a\sin\theta\bigr),\qquad b>a>0.
$$

内在的に平坦な商空間としてのトーラスとは異なり、この埋め込み
トーラスの曲率は場所によって符号が変わります。ここでは接続、
リーマンテンソル、リッチテンソル、スカラー曲率を計算します。

<!-- cell: 8b3592df -->
## 座標と計量

座標ベクトルは互いに直交し、その長さの2乗は$a^2$と
$(b+a\cos\theta)^2$です。したがって、

$$
g=\begin{pmatrix}a^2&0\\0&(b+a\cos\theta)^2\end{pmatrix}.
$$

<!-- cell: 62ffcc8b -->
## レヴィ・チヴィタ接続

次の式を用い、第1添字を$g^{ij}$で上げます。
$\Gamma_{ijk}=\tfrac12(\partial_jg_{ik}+\partial_kg_{ij}-\partial_ig_{jk})$

<!-- cell: bfea5de7 -->
## リーマンテンソル

末尾の2つの添字は反対称です。第1添字を下げると、$R_{ijkl}$で
よく知られた添字対の対称性も明らかになります。

<!-- cell: afa384c7 -->
## リッチ曲率・スカラー曲率・ガウス曲率

2次元では、スカラー曲率はガウス曲率の2倍、すなわち
$\mathcal R=2K$です。このトーラスでは、

$$
K(\theta)=\frac{\cos\theta}{a(b+a\cos\theta)}.
$$

<!-- cell: 9b9496b2 -->
## 幾何学的な意味

トーラスの外側（$\cos\theta>0$）では曲率が正、内側
（$\cos\theta<0$）では負となり、上端と下端の円周上では曲率が0で
放物的になります。
ガウス–ボンネ積分では正負の寄与が打ち消し合い、
$\chi(T^2)=0$と整合します。
