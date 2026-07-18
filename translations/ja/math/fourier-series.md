<!--
notebook: fourier-series
source-markdown-sha256: 9b3482351255dbdc0505898977f7c1d3e37a0a4dd53a8fccef73599783a38a20
-->

<!-- cell: 3afbe59d -->
# のこぎり波のフーリエ級数

$-\pi<x<\pi$で$f(x)=x$と定め、それを$2\pi$周期で拡張した
関数を考えます。そのフーリエ級数は

$$
f(x)\sim \frac{a_0}{2}
  +\sum_{k=1}^{\infty}a_k\cos(kx)
  +\sum_{k=1}^{\infty}b_k\sin(kx).
$$

Egisonで係数を与える積分を記号的に計算し、級数の最初の数項を
組み立てます。

<!-- cell: bef7916d -->
## 原始関数の記号計算

係数は次の積分で与えられます。

$$
a_k=\frac1\pi\int_{-\pi}^{\pi}x\cos(kx)\,dx,
\qquad
b_k=\frac1\pi\int_{-\pi}^{\pi}x\sin(kx)\,dx.
$$

部分積分により、$x\cos(kx)$と$x\sin(kx)$の原始関数を明示的に
求められます。ここではその公式を直接定義し、このNotebookが
追加の積分ライブラリに依存しないようにします。

<!-- cell: 28ee912d -->
## フーリエ係数

のこぎり波は奇関数なので、余弦係数はすべて0です。正弦係数は
$b_k=2(-1)^{k+1}/k$となります。

<!-- cell: a3ef0cbd -->
## フーリエ級数の再構成

各$b_k$に$\sin(kx)$を掛けると、フーリエ級数の各項が順に得られます。

<!-- cell: 8f1ad57d -->
したがって、

$$
x=2\sum_{k=1}^{\infty}\frac{(-1)^{k+1}}{k}\sin(kx)
\qquad(-\pi<x<\pi).
$$

関数の偶奇性と係数の計算を別々のセルにすることで、余弦項が
一つも残らない理由が明確になります。
