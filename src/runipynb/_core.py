import inspect
import os
import pathlib
from contextlib import contextmanager, nullcontext
from typing import Iterator

import nbformat
from IPython.core.interactiveshell import InteractiveShell


@contextmanager
def _chdir(path: pathlib.Path) -> Iterator[None]:
    old = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


def run_notebook(
    path: str | os.PathLike,
    ns: dict | None = None,
    *,
    raise_on_error: bool = True,
    chdir: bool = True,
) -> dict:
    if ns is None:
        ns = inspect.currentframe().f_back.f_globals  # type: ignore[union-attr]

    nb_path = pathlib.Path(path).resolve()
    nb = nbformat.read(nb_path, as_version=4)

    # Use the singleton so get_ipython() works inside cells.
    shell = InteractiveShell.instance(user_ns=ns)
    shell.user_ns = ns

    # chdir to the notebook's directory so relative paths inside cells
    # (e.g. pd.read_csv("data.csv")) resolve the same way they would in Jupyter.
    cm = _chdir(nb_path.parent) if chdir else nullcontext()
    with cm:
        for cell in nb.cells:
            if cell.cell_type != "code":
                continue
            result = shell.run_cell(cell.source, store_history=False)
            if raise_on_error and not result.success:
                exc = result.error_in_exec or result.error_before_exec
                if exc is None:
                    raise RuntimeError("cell failed with no exception captured")
                raise exc

    return ns
