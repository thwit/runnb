"""
Demonstrates running a notebook into the caller's globals.

Run from the repo root:
    python examples/demo.py
"""

import runnb

runnb.run_notebook("tests/fixtures/with_magics.ipynb")

print("###")
print(helper_var)   # noqa: F821  — defined inside the notebook
print("###")
print(result)       # noqa: F821
print("###")
print(shell_out)    # noqa: F821
