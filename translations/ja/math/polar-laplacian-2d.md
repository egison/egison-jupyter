<!--
notebook: polar-laplacian-2d
source-markdown-sha256: bc106c96d5daf6d542d4b8889f8b1f0da282dae14a8d19ef21fd50b1d0e67be8
-->

<!-- cell: eaaca8cc -->
# 2次元極座標のラプラシアン

ユークリッド空間のラプラシアンが表す意味は座標によらない一方、
その具体的な式は座標によって変わります。ここでは計量から
極座標表示を導出し、多変数の連鎖律を使って検算します。

<!-- cell: e05e246b -->
## 座標と計量

線素は次のように表されます。

$$ds^2=dr^2+r^2d\theta^2$$

計量とその逆計量を添字付きテンソルとして表現します。

<!-- cell: be39a592 -->
## 共変微分による導出

スカラー場に対するラプラス–ベルトラミ作用素は次のように書けます。

$$
\Delta f=g^{ij}\partial_i\partial_jf
   -g^{ij}\Gamma^k{}_{ij}\partial_kf.
$$

Egisonは、この式に現れる重複したテンソル添字をそのまま縮約します。

<!-- cell: 8d604e97 -->
## 計算結果

$$
\Delta f=\frac{\partial^2f}{\partial r^2}
  +\frac1r\frac{\partial f}{\partial r}
  +\frac1{r^2}\frac{\partial^2f}{\partial\theta^2}.
$$

<!-- cell: 95e59a45 -->
## 連鎖律による検算

最後に、2変数の直交座標関数を新しい座標の関数とみなします。
上に示した座標表示を展開すると、すべての混合偏微分が打ち消し合い、
直交座標のラプラシアンだけが残るはずです。

<!-- cell: 73d938bb -->
展開結果は$u_{XX}+u_{YY}$となります。これにより、角度方向の
尺度の変化が$r^{-1}u_r$の項によって補正されることが確認できます。
