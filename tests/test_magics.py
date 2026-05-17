"""
Comprehensive magic support test suite for runipynb.

Each test documents one magic and verifies it works end-to-end through
run_notebook(), with a verifiable side effect in the namespace.
"""

import pathlib

import pytest

import runipynb

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# Cell magics  (%%magic)
# ---------------------------------------------------------------------------


def test_cell_magic_capture():
    """%%capture stores stdout in a RichOutput object in the namespace."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "cell_magic_capture.ipynb", ns=ns)
    assert "hello capture" in ns["captured_text"]
    assert "line two" in ns["captured_text"]


def test_cell_magic_writefile():
    """%%writefile writes cell body to disk; subsequent cells can read it back."""
    out_file = FIXTURES / "_writefile_out.txt"
    ns = {}
    try:
        runipynb.run_notebook(FIXTURES / "cell_magic_writefile.ipynb", ns=ns)
        assert "hello from writefile" in ns["writefile_content"]
        assert "line two" in ns["writefile_content"]
    finally:
        out_file.unlink(missing_ok=True)


def test_cell_magic_html():
    """%%html is a display-only magic; it must not raise and execution continues."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "cell_magic_html.ipynb", ns=ns)
    assert ns["html_ran"] is True


def test_cell_magic_markdown():
    """%%markdown is a display-only magic; it must not raise and execution continues."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "cell_magic_markdown.ipynb", ns=ns)
    assert ns["markdown_ran"] is True


def test_cell_magic_timeit():
    """%%timeit runs the cell body for timing; execution continues afterwards."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "cell_magic_timeit.ipynb", ns=ns)
    assert ns["timeit_ran"] is True


# ---------------------------------------------------------------------------
# Line magics  (%magic)
# ---------------------------------------------------------------------------


def test_line_magic_timeit():
    """%timeit -o returns a TimeitResult object that can be assigned."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "line_magic_timeit.ipynb", ns=ns)
    best = ns["timeit_result_best"]
    assert isinstance(best, float)
    assert best >= 0


def test_line_magic_who_ls():
    """%who_ls returns a list of user-defined variable names in the namespace."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "line_magic_who_ls.ipynb", ns=ns)
    assert "sentinel" in ns["ns_names"]


def test_line_magic_env():
    """%env VAR=value sets an environment variable readable via os.environ."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "line_magic_env.ipynb", ns=ns)
    assert ns["env_result"] == "runnb_magic_env_value"


def test_line_magic_pwd():
    """%pwd returns the current working directory as a string."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "line_magic_pwd.ipynb", ns=ns)
    cwd = ns["cwd_result"]
    assert isinstance(cwd, str)
    assert len(cwd) > 0


def test_line_magic_load_ext():
    """%load_ext loads an IPython extension (autoreload) without error."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "line_magic_load_ext.ipynb", ns=ns)
    assert ns["load_ext_ran"] is True


def test_line_magic_sx():
    """%sx (alias: %system) runs a shell command and returns output as a list."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "line_magic_sx.ipynb", ns=ns)
    assert ns["sx_result"] == "hello_from_sx"


def test_line_magic_set_env():
    """%set_env VAR=value sets an environment variable (alternative syntax to %env)."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "line_magic_set_env.ipynb", ns=ns)
    assert ns["set_env_result"] == "set_env_worked"


def test_line_magic_alias_magic():
    """%alias_magic creates a new magic alias; the alias is immediately callable."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "line_magic_alias_magic.ipynb", ns=ns)
    assert isinstance(ns["alias_magic_best"], float)
    assert ns["alias_magic_best"] >= 0


def test_line_magic_xdel():
    """%xdel removes a variable from the namespace and clears all references."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "line_magic_xdel.ipynb", ns=ns)
    assert "doomed" not in ns
    assert ns["survived"] == 1


def test_line_magic_reset_selective():
    """%reset_selective -f <regex> removes matching variables, leaves others intact."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "line_magic_reset_selective.ipynb", ns=ns)
    assert "keep_me" in ns
    assert "remove_me" not in ns


def test_line_magic_psearch():
    """%psearch <pattern> searches the namespace by wildcard; display-only, must not raise."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "line_magic_psearch.ipynb", ns=ns)
    assert ns["psearch_ran"] is True


def test_line_magic_xmode():
    """%xmode switches the exception display mode (Minimal / Context / Verbose)."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "line_magic_xmode.ipynb", ns=ns)
    assert ns["xmode_ran"] is True


def test_line_magic_ext_lifecycle():
    """%reload_ext and %unload_ext complete the extension load/reload/unload cycle."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "line_magic_ext_lifecycle.ipynb", ns=ns)
    assert ns["ext_lifecycle_ran"] is True


# ---------------------------------------------------------------------------
# Additional cell magics
# ---------------------------------------------------------------------------


def test_cell_magic_svg():
    """%%svg is a display-only magic; it must not raise and execution continues."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "cell_magic_svg.ipynb", ns=ns)
    assert ns["svg_ran"] is True


def test_cell_magic_latex():
    """%%latex is a display-only magic; it must not raise and execution continues."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "cell_magic_latex.ipynb", ns=ns)
    assert ns["latex_ran"] is True


def test_cell_magic_javascript():
    """%%javascript and %%js (alias) are display-only; both must not raise."""
    ns = {}
    runipynb.run_notebook(FIXTURES / "cell_magic_javascript.ipynb", ns=ns)
    assert ns["javascript_ran"] is True
    assert ns["js_alias_ran"] is True
