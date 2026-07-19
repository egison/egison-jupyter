<!--
notebook: polar-laplacian-3d
source-markdown-sha256: d90abdb12b98dd8da80bfbce2823ef1669da11843a4512c9504a5f8c65237664
-->

<!-- cell: a22f0542 -->
# 球座標のラプラシアン

ユークリッド空間のラプラシアンが表す意味は座標によらない一方、
その具体的な式は座標によって変わります。ここでは計量から
球座標表示を導出し、多変数の連鎖律を使って検算します。

<!-- cell: 0149855e -->
## 座標と計量

線素は次のように表されます。

$$ds^2=dr^2+r^2d\theta^2+r^2\sin^2\theta\,d\phi^2.$$

座標写像を微分して接ベクトルを求め、それらの内積から計量を構成します。
逆計量は、この誘導計量の行列から計算します。

<!-- cell: 407069d9 -->
## 共変微分による導出

スカラー場に対するラプラス–ベルトラミ作用素は次のように書けます。

$$
\Delta f=g^{ij}\partial_i\partial_jf
   -g^{ij}\Gamma^k{}_{ij}\partial_kf.
$$

Egisonは、この式に現れる重複したテンソル添字をそのまま縮約します。

<!-- cell: b628bf7c -->
## 計算結果

$$
\Delta f=\frac{\partial^2f}{\partial r^2}
  +\frac2r\frac{\partial f}{\partial r}
  +\frac1{r^2}\frac{\partial^2f}{\partial\theta^2}
  +\frac{\cos\theta}{r^2\sin\theta}\frac{\partial f}{\partial\theta}
  +\frac1{r^2\sin^2\theta}\frac{\partial^2f}{\partial\phi^2}.
$$

<!-- cell: 81e81f98 -->
## 連鎖律による検算

最後に、3変数の直交座標関数を新しい座標の関数とみなします。
上に示した座標表示を展開すると、すべての混合偏微分が打ち消し合い、
直交座標のラプラシアンだけが残るはずです。

<!-- cell: e95589e1 -->
展開結果は$u_{XX}+u_{YY}+u_{ZZ}$となります。1階微分を含む各項は、
動径方向と角度方向の尺度因子の変化によって生じる補正に
ちょうど対応しています。
