import inspect
import os
import pathlib
from contextlib import contextmanager, nullcontext

import nbformat
from IPython.core.interactiveshell import InteractiveShell


@contextmanager
def _chdir(path):
    old = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


def run_notebook(path, ns=None, *, raise_on_error=True, chdir=True):
    if ns is None:
        ns = inspect.currentframe().f_back.f_globals

    nb_path = pathlib.Path(path).resolve()
    nb = nbformat.read(nb_path, as_version=4)

    # Use the singleton so get_ipython() works inside cells.
    shell = InteractiveShell.instance(user_ns=ns)
    # If the singleton already existed with a different ns, rebind it.
    shell.user_ns = ns

    cm = _chdir(nb_path.parent) if chdir else nullcontext()
    with cm:
        for cell in nb.cells:
            if cell.cell_type != "code":
                continue
            result = shell.run_cell(cell.source, store_history=False)
            if raise_on_error and not result.success:
                raise (result.error_in_exec or result.error_before_exec)

    return ns
