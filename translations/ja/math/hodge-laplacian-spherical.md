<!--
notebook: hodge-laplacian-spherical
source-markdown-sha256: 03b7e1b836655d4bd8ecd9d7dadd492add7317c6f258bc7be66621f1842fb948
-->

<!-- cell: 96c3442e -->
# 球座標のホッジラプラシアン

球座標 $(r,\theta,\phi)$ におけるユークリッド計量は

$$ds^2=dr^2+r^2d\theta^2+r^2\sin^2\theta\,d\phi^2.$$

です。この計量から $d$、$\star$、余微分を構成します。以下で採用する
余微分の規約では、スカラーに対する結果は通常の座標表示による
正符号のラプラス作用素に負号を付けたものになります。

<!-- cell: 80c07a49 -->
## 球座標の計量

計量の行列式は $r^4\sin^2\theta$ です。一方、逆計量には角度方向の
尺度因子 $r^{-2}$ と $(r^2\sin^2\theta)^{-1}$ が含まれます。

<!-- cell: c00a1543 -->
## 微分形式の演算子

ホッジスターは $g^{ij}$ で形式の添字を上げ、3次元の
レヴィ・チヴィタテンソルと縮約します。

<!-- cell: 08fa7851 -->
ホッジラプラシアンは $d\delta+\delta d$ です。スカラーと体積形式には、
より短い端点の公式を用います。

<!-- cell: a1f2e150 -->
式を簡約すると、出力は

$$
\Delta f=-\left(
f_{rr}+\frac{2}{r}f_r
+\frac1{r^2}f_{\theta\theta}
+\frac{\cos\theta}{r^2\sin\theta}f_\theta
+\frac1{r^2\sin^2\theta}f_{\phi\phi}
\right).
$$

となります。座標に依存する各係数はすべて計量から導かれており、
球座標のラプラシアンの公式そのものは計算への入力として使っていません。
