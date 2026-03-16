# philiprehberger-deprecate

[![Tests](https://github.com/philiprehberger/py-deprecate/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-deprecate/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-deprecate.svg)](https://pypi.org/project/philiprehberger-deprecate/)
[![License](https://img.shields.io/github/license/philiprehberger/py-deprecate)](LICENSE)

Decorator and utilities for deprecating functions, parameters, and classes with zero boilerplate.

## Install

```bash
pip install philiprehberger-deprecate
```

## Usage

```python
from philiprehberger_deprecate import deprecated, deprecated_class, deprecated_param
```

### Deprecate a function

```python
@deprecated(remove_in="2.0.0", alternative="new_fetch")
def old_fetch(url: str) -> str:
    ...
```

Calling `old_fetch()` emits:

```
DeprecationWarning: Function 'old_fetch' is deprecated. Will be removed in 2.0.0. Use 'new_fetch' instead.
```

### Deprecate a parameter

```python
@deprecated_param("color", renamed_to="colour", remove_in="2.0.0")
def draw(shape: str, *, colour: str = "red") -> None:
    ...

draw(shape="circle", color="blue")  # warns and forwards color -> colour
```

### Deprecate a class

```python
@deprecated_class(remove_in="3.0.0", alternative="NewClient")
class OldClient:
    def __init__(self, host: str) -> None:
        self.host = host
```

Instantiating `OldClient()` emits a `DeprecationWarning`.

## API

| Function | Description |
|---|---|
| `deprecated(remove_in, *, alternative, message)` | Function decorator that emits `DeprecationWarning` on each call |
| `deprecated_param(param, *, renamed_to, remove_in)` | Function decorator that warns when a deprecated parameter is passed and optionally maps it to its replacement |
| `deprecated_class(remove_in, *, alternative, message)` | Class decorator that emits `DeprecationWarning` on instantiation |

## License

MIT
