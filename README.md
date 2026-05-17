# runnb

Run a Jupyter notebook into your script's namespace — with full IPython magic support.

## Install

```bash
pip install runnb
```

## Usage

```python
import runnb

# Variables, functions, and imports from the notebook land in your script's globals.
runnb.run_notebook("analysis.ipynb")
print(result)  # defined in the notebook

# Or run into an explicit dict.
ns = {}
runnb.run_notebook("analysis.ipynb", ns=ns)
print(ns["result"])
```

## How it works

`runnb` wires your script's `globals()` dict directly into an IPython `InteractiveShell` and
executes each code cell with `shell.run_cell()`. This is the same execution path Jupyter itself
uses, so line magics (`%run`, `%matplotlib`), cell magics (`%%time`, `%%capture`), and shell
escapes (`!ls`) all work exactly as they would inside a notebook. No subprocess, no separate
kernel — the notebook runs in the same Python process as your script, sharing the same namespace.
