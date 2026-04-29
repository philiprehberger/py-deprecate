# Changelog

## 0.2.0 (2026-04-29)

- Add `deprecated_module(name, ...)` helper to flag deprecated modules at import time
- Replace import-only stub with real test suite covering all four helpers
- Clean up malformed CHANGELOG history (collapsed `0.1.6` entry split out)

## 0.1.7 (2026-03-31)

- Standardize README to 3-badge format with emoji Support section
- Update CI checkout action to v5 for Node.js 24 compatibility
- Add GitHub issue templates, dependabot config, and PR template

## 0.1.6

- Add pytest and mypy tool configuration to pyproject.toml

## 0.1.5

- Add basic import test

## 0.1.4

- Add Development section to README

## 0.1.1

- Re-release for PyPI publishing

## 0.1.0 (2026-03-15)

- Initial release
- `deprecated` decorator for functions
- `deprecated_param` decorator for warning on deprecated parameter usage with optional rename mapping
- `deprecated_class` decorator for warning on class instantiation
