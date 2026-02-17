# Egison Kernel for Jupyter

A Jupyter kernel for the [Egison](https://www.egison.org) programming language (version 5).

Provides syntax highlighting in Jupyter notebooks via a CodeMirror mode that supports Egison 5 syntax including type classes, inductive data types, type annotations, and pattern matching.

## How to Install

### 1. Create a Python virtual environment and install dependencies

```sh
cd egison-jupyter
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install .
```

### 2. Install Jupyter and the Egison kernel

```sh
pip install jupyter
python -m egison_kernel.install
```

### 3. (Optional) Install the CodeMirror mode for syntax highlighting

Copy the CodeMirror mode file to Jupyter's CodeMirror directory:

```sh
JUPYTER_DIR=$(jupyter --data-dir)
mkdir -p "$JUPYTER_DIR/nbextensions/codemirror/mode/egison"
cp codemirror/mode/egison/egison.js "$JUPYTER_DIR/nbextensions/codemirror/mode/egison/"
```

## How to Use

Make sure the virtual environment is activated, then start Jupyter:

```sh
source .venv/bin/activate
jupyter notebook
# In the notebook interface, select Egison from the 'New' menu
```

<img width="100%" src="https://raw.githubusercontent.com/egison/egison_kernel/master/images/RiemannCurvatureOfS2.png" />

## Syntax Highlighting

The CodeMirror mode supports Egison 5 syntax:

- Type system keywords: `class`, `instance`, `inductive`, `extends`, `declare`
- Definition keywords: `def`, `let`, `in`, `where`
- Pattern matching: `match`, `matchAll`, `matchDFS`, `matchAllDFS`, `as`, `with`, `loop`, `forall`
- Built-in types: `Integer`, `MathExpr`, `Float`, `Bool`, `Char`, `String`, `IO`, `Tensor`, `Vector`, `Matrix`, `DiffForm`, `Matcher`, `Pattern`, `List`
- Pattern variables (`$x`), value patterns (`#x`)
- Comments: line comments (`--`) and nested block comments (`{- -}`)
- Tensor index notation, mathematical symbols, and Greek letters

## Requirements

- Egison 5.x installed and available in PATH
- Python 3
- Jupyter Notebook or JupyterLab

## Acknowledgement

I learned how to implement a Jupyter kernel from [bash_kernel](https://github.com/takluyver/bash_kernel).

I thank Shunsuke Gotoh for [his article](https://qiita.com/antimon2/items/7d9c084b142d38b67b1f) on the initial Python program of this kernel.
