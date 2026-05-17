# Changelog

## 0.1.0 — 2026-05-17

Initial release.

- `run_notebook(path, ns, *, raise_on_error, chdir)` — execute a Jupyter notebook
  in-process via IPython's `InteractiveShell`
- Full support for IPython line magics (`%run`, `%timeit`, `%env`, …), cell magics
  (`%%time`, `%%capture`, `%%writefile`, …), and shell escapes (`!cmd`)
- 31 tests covering core behaviour and 22 specific magics
