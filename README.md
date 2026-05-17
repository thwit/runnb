# runipynb

[![CI](https://github.com/thwit/runnb/actions/workflows/ci.yml/badge.svg)](https://github.com/thwit/runnb/actions/workflows/ci.yml)

Run a Jupyter notebook into your script's namespace — with full IPython magic support.

## Install

```bash
pip install runipynb
```

## Usage

```python
import runipynb

# Variables, functions, and imports from the notebook land in your script's globals.
runipynb.run_notebook("analysis.ipynb")
print(result)  # defined in the notebook

# Or run into an explicit dict.
ns = {}
runipynb.run_notebook("analysis.ipynb", ns=ns)
print(ns["result"])
```

## Magic support

Because `runipynb` uses IPython's `InteractiveShell` internally, all built-in IPython magics work out of the box. The table below covers the most commonly used ones, with notes on what you can observe in the namespace after the cell runs.

### Cell magics (`%%`)

| Magic | Supported | Test | Notes |
|---|---|---|---|
| `%%time` | Yes | `test_cell_magic_time` | Prints timing; cell body executes normally, variables persist |
| `%%timeit` | Yes | `test_cell_magic_timeit` | Prints timing stats; body runs in isolation, variables do **not** persist |
| `%%capture <var>` | Yes | `test_cell_magic_capture` | Stdout/stderr stored in `<var>.stdout` / `<var>.stderr` in the namespace |
| `%%writefile <path>` | Yes | `test_cell_magic_writefile` | Writes cell body to `<path>`; respects `chdir=True` |
| `%%html` | Yes | `test_cell_magic_html` | Display-only; no namespace side effects |
| `%%markdown` | Yes | `test_cell_magic_markdown` | Display-only; no namespace side effects |
| `%%svg` | Yes | `test_cell_magic_svg` | Display-only; no namespace side effects |
| `%%latex` | Yes | `test_cell_magic_latex` | Display-only; no namespace side effects |
| `%%javascript` / `%%js` | Yes | `test_cell_magic_javascript` | Display-only; no namespace side effects |
| `%%bash` / `%%sh` | Platform | — | Requires bash on `PATH`; works on Linux/macOS, may fail on Windows |
| `%%cmd` | Windows only | — | Windows `cmd.exe` shell; not available on Linux/macOS |
| `%%script <cmd>` | Yes | — | Runs cell body via the given interpreter |
| `%%python` / `%%python3` | Yes | — | Runs body in a subprocess; variables do **not** persist |
| `%%capture` (no var) | Yes | — | Silently swallows output; nothing added to namespace |

### Line magics (`%`)

| Magic | Supported | Test | Notes |
|---|---|---|---|
| `%run <file>` | Yes | `test_line_magic_run` | Executes `.py` or `.ipynb`; definitions land in the shared namespace |
| `%timeit [-o] <stmt>` | Yes | `test_line_magic_timeit` | With `-o`, returns a `TimeitResult` that can be assigned |
| `%who_ls` | Yes | `test_line_magic_who_ls` | Returns list of user-defined names currently in the namespace |
| `%env VAR=value` | Yes | `test_line_magic_env` | Sets environment variable; visible to `os.environ` immediately |
| `%set_env VAR=value` | Yes | `test_line_magic_set_env` | Alternative env-var setter; same effect as `%env VAR=value` |
| `%pwd` | Yes | `test_line_magic_pwd` | Returns current working directory as a string |
| `%load_ext <ext>` | Yes | `test_line_magic_load_ext` | Loads an IPython extension (e.g. `autoreload`) |
| `%reload_ext <ext>` | Yes | `test_line_magic_ext_lifecycle` | Reloads a previously loaded extension |
| `%unload_ext <ext>` | Yes | `test_line_magic_ext_lifecycle` | Unloads a previously loaded extension |
| `%sx <cmd>` / `%system` | Yes | `test_line_magic_sx` | Explicit shell-capture magic; identical semantics to `!<cmd>` |
| `%alias_magic <name> <magic>` | Yes | `test_line_magic_alias_magic` | Creates a new magic alias; alias is immediately callable |
| `%xdel <var>` | Yes | `test_line_magic_xdel` | Deletes a variable and clears all references to it |
| `%reset_selective -f <regex>` | Yes | `test_line_magic_reset_selective` | Removes variables matching regex; leaves non-matching ones intact |
| `%psearch <pattern>` | Yes | `test_line_magic_psearch` | Searches namespace by wildcard; display-only |
| `%xmode <mode>` | Yes | `test_line_magic_xmode` | Switches exception display mode (`Minimal` / `Context` / `Verbose`) |
| `%matplotlib <backend>` | Yes | — | Sets matplotlib backend; requires `matplotlib` installed |
| `%cd <path>` | Yes | — | Changes the shell's working directory (persists after the cell) |
| `%pinfo <obj>` / `%pinfo2` | Yes | — | Prints docstring / source; no namespace side effects |
| `!<cmd>` (shell escape) | Yes | `test_shell_escape` | Runs shell command; assign to capture output as a list of lines |

## How it works

`runipynb` wires your script's `globals()` dict directly into an IPython `InteractiveShell` and
executes each code cell with `shell.run_cell()`. This is the same execution path Jupyter itself
uses, so line magics (`%run`, `%matplotlib`), cell magics (`%%time`, `%%capture`), and shell
escapes (`!ls`) all work exactly as they would inside a notebook. No subprocess, no separate
kernel — the notebook runs in the same Python process as your script, sharing the same namespace.
