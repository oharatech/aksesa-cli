# CLI Loading Time

## `src/aksesa_cli/__init__.py` be empty

**Scope**

`src/aksesa_cli/__init__.py`

**Requirements**

The `src/aksesa_cli/__init__.py` file must be empty, containing no code or imports.

## No unnecessary import in `src/aksesa_cli/cli.py`

**Scope**

`src/aksesa_cli/cli.py`

**Requirements**

The `src/aksesa_cli/cli.py` file must not import any modules from `aksesa_cli` or `kosong`, except for `aksesa_cli.constant`, at the top level.

## As-needed imports in `src/aksesa_cli/app.py`

**Scope**

`src/aksesa_cli/app.py`

**Requirements**

The `src/aksesa_cli/app.py` file must not import any modules prefixed with `aksesa_cli.ui` at the top level; instead, UI-specific modules should be imported within functions as needed.

<examples>

```python
# top-level
from aksesa_cli.ui.shell import ShellApp  # Incorrect: top-level import of UI module

# inside function
async def run_shell_app(...):
    from aksesa_cli.ui.shell import ShellApp  # Correct: import as needed
    app = ShellApp(...)
    await app.run()
```

</examples>

## `--help` should run fast

**Scope**

No specific source file.

**Requirements**

The time taken to run `uv run kimi --help` must be less than 150 milliseconds on average over 5 runs after a 3-run warm-up.
