import os
import pathlib

import pytest

import runipynb

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


def test_basic_into_caller_globals():
    runipynb.run_notebook(FIXTURES / "basic.ipynb")
    g = globals()
    assert g["x"] == 42
    assert callable(g["double"])
    assert g["y"] == 84


def test_explicit_ns():
    ns = {}
    runipynb.run_notebook(FIXTURES / "basic.ipynb", ns=ns)
    assert ns["x"] == 42
    assert callable(ns["double"])
    assert ns["y"] == 84
    assert "x" not in globals() or globals().get("x") == 42  # caller globals unchanged


def test_line_magic_run():
    ns = {}
    runipynb.run_notebook(FIXTURES / "with_magics.ipynb", ns=ns)
    assert ns["helper_var"] == "loaded from helper.py"
    assert callable(ns["helper_fn"])
    assert ns["result"] == 50


def test_shell_escape():
    ns = {}
    runipynb.run_notebook(FIXTURES / "with_magics.ipynb", ns=ns)
    assert ns["shell_out"][0].strip() == "hello_from_shell"


def test_cell_magic_time():
    ns = {}
    runipynb.run_notebook(FIXTURES / "with_magics.ipynb", ns=ns)
    assert ns["timed"] is True


def test_chdir_default(tmp_path):
    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        ns = {}
        runipynb.run_notebook(FIXTURES / "reads_local_file.ipynb", ns=ns)
        assert ns["rows"][0] == ["a", "b"]
    finally:
        os.chdir(original_cwd)


def test_chdir_false(tmp_path):
    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        with pytest.raises(FileNotFoundError):
            runipynb.run_notebook(FIXTURES / "reads_local_file.ipynb", chdir=False)
    finally:
        os.chdir(original_cwd)


def test_raise_on_error():
    ns = {}
    with pytest.raises(ValueError, match="boom"):
        runipynb.run_notebook(FIXTURES / "raises.ipynb", ns=ns)
    assert ns["before"] == 1
    assert "after" not in ns


def test_keep_going():
    ns = {}
    runipynb.run_notebook(FIXTURES / "raises.ipynb", ns=ns, raise_on_error=False)
    assert ns["before"] == 1
    assert ns["after"] == 2


def test_returns_ns():
    ns = {}
    result = runipynb.run_notebook(FIXTURES / "basic.ipynb", ns=ns)
    assert result is ns
