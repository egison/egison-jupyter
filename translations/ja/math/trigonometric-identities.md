<!--
notebook: trigonometric-identities
source-markdown-sha256: 66f54566ea81b6802b0b5fb4051fad19168ea0c5b8e0357ce91a713097975ddb
-->

<!-- cell: 2eaf7e55 -->
# 複素数の乗法から導く三角関数の恒等式

オイラーの公式を使うと、余弦と正弦を一つの代数的な式にまとめられます。

$$u(\alpha)=\cos\alpha+i\sin\alpha=e^{i\alpha}.$$

これらの式を掛け合わせ、実部と虚部の係数を読むことで、よく知られた
いくつかの恒等式を導けます。一度の多項式計算を行い、その係数を
解釈するという、記号計算に有用なパターンです。

<!-- cell: ea90c735 -->
## 単位円上の式の記号表現

$\alpha$と$\beta$は記号のまま扱います。式`uMinusBeta`は、
簡約器に正弦と余弦の偶奇性を認識させることなく、
$u(-\beta)=\cos\beta-i\sin\beta$を表します。

<!-- cell: 9864f158 -->
## 加法定理

$u(\alpha)u(\beta)$における$1$と$i$の係数は、それぞれ
$\cos(\alpha+\beta)$と$\sin(\alpha+\beta)$です。

<!-- cell: c30677bd -->
返された2つの係数を読むと、次の式が得られます。

$$
\cos(\alpha+\beta)=\cos\alpha\cos\beta-\sin\alpha\sin\beta,
$$
$$
\sin(\alpha+\beta)=\sin\alpha\cos\beta+\cos\alpha\sin\beta.
$$

$u(\alpha)u(\beta)$と$u(\alpha)u(-\beta)$を加えると、積和公式に
現れる組合せだけを取り出せます。

<!-- cell: 90fe2b1c -->
結果の実部は$2\cos\alpha\cos\beta$、虚部は
$2\sin\alpha\cos\beta$を表します。2で割り、2つの積を
$u(\alpha\pm\beta)$で置き換えると、標準的な積和公式が得られます。

## 三倍角の公式

単位円上の式を3乗すると、二項展開のすべての項を一度に計算できます。

<!-- cell: 09c68e68 -->
実部と虚部はそれぞれ

$$\cos^3\alpha-3\cos\alpha\sin^2\alpha,$$
$$3\cos^2\alpha\sin\alpha-\sin^3\alpha.$$

第1式に$\sin^2\alpha=1-\cos^2\alpha$を、第2式に
$\cos^2\alpha=1-\sin^2\alpha$を用いると、

$$\cos(3\alpha)=4\cos^3\alpha-3\cos\alpha,$$
$$\sin(3\alpha)=3\sin\alpha-4\sin^3\alpha.$$

重要なのは、Egisonの係数抽出によって、あらかじめ与えた恒等式を
単に検算するのではなく、複素数の乗法から式を見通しよく
導出できることです。
