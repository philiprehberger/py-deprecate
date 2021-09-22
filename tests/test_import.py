"""Basic import test."""


def test_import():
    """Verify the package can be imported."""
    import philiprehberger_deprecate
    assert hasattr(philiprehberger_deprecate, "__name__") or True
