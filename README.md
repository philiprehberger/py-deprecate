# philiprehberger-deprecate

[![Tests](https://github.com/philiprehberger/py-deprecate/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-deprecate/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-deprecate.svg)](https://pypi.org/project/philiprehberger-deprecate/)
[![Last updated](https://img.shields.io/github/last-commit/philiprehberger/py-deprecate)](https://github.com/philiprehberger/py-deprecate/commits/main)

Decorator and utilities for deprecating functions, parameters, and classes with zero boilerplate.

## Installation

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

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## Support

If you find this project useful:

⭐ [Star the repo](https://github.com/philiprehberger/py-deprecate)

🐛 [Report issues](https://github.com/philiprehberger/py-deprecate/issues?q=is%3Aissue+is%3Aopen+label%3Abug)

💡 [Suggest features](https://github.com/philiprehberger/py-deprecate/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)

❤️ [Sponsor development](https://github.com/sponsors/philiprehberger)

🌐 [All Open Source Projects](https://philiprehberger.com/open-source-packages)

💻 [GitHub Profile](https://github.com/philiprehberger)

🔗 [LinkedIn Profile](https://www.linkedin.com/in/philiprehberger)

## License

[MIT](LICENSE)
