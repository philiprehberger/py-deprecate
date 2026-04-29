"""Tests for philiprehberger_deprecate."""

from __future__ import annotations

import warnings

import pytest

from philiprehberger_deprecate import (
    deprecated,
    deprecated_class,
    deprecated_module,
    deprecated_param,
)


class TestDeprecatedFunction:
    def test_emits_warning(self) -> None:
        @deprecated()
        def old() -> int:
            return 1

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            assert old() == 1
        assert len(caught) == 1
        assert issubclass(caught[0].category, DeprecationWarning)
        assert "old" in str(caught[0].message)

    def test_remove_in_in_message(self) -> None:
        @deprecated(remove_in="2.0.0")
        def f() -> None:
            pass

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            f()
        assert "2.0.0" in str(caught[0].message)

    def test_alternative_in_message(self) -> None:
        @deprecated(alternative="new_func")
        def f() -> None:
            pass

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            f()
        assert "new_func" in str(caught[0].message)

    def test_custom_message_overrides(self) -> None:
        @deprecated(remove_in="2.0", alternative="x", message="custom note")
        def f() -> None:
            pass

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            f()
        assert str(caught[0].message) == "custom note"

    def test_preserves_metadata(self) -> None:
        @deprecated()
        def my_function() -> None:
            """My docstring."""

        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "My docstring."

    def test_passes_args_through(self) -> None:
        @deprecated()
        def add(a: int, b: int) -> int:
            return a + b

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            assert add(2, 3) == 5


class TestDeprecatedParam:
    def test_warns_when_used(self) -> None:
        @deprecated_param("old_name", renamed_to="new_name")
        def f(*, new_name: int = 0) -> int:
            return new_name

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            result = f(old_name=5)
        assert result == 5
        assert any("old_name" in str(w.message) for w in caught)

    def test_no_warning_when_unused(self) -> None:
        @deprecated_param("old_name", renamed_to="new_name")
        def f(*, new_name: int = 0) -> int:
            return new_name

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            f(new_name=5)
        assert caught == []

    def test_remove_in_in_message(self) -> None:
        @deprecated_param("old", remove_in="3.0")
        def f(*, old: int = 0) -> None:
            pass

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            f(old=1)
        assert "3.0" in str(caught[0].message)


class TestDeprecatedClass:
    def test_warns_on_instantiation(self) -> None:
        @deprecated_class(remove_in="2.0", alternative="NewClass")
        class OldClass:
            def __init__(self, x: int) -> None:
                self.x = x

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            obj = OldClass(42)
        assert obj.x == 42
        assert "OldClass" in str(caught[0].message)
        assert "2.0" in str(caught[0].message)
        assert "NewClass" in str(caught[0].message)


class TestDeprecatedModule:
    def test_emits_warning(self) -> None:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            deprecated_module("mypkg.legacy", remove_in="2.0.0", alternative="mypkg.modern")
        assert len(caught) == 1
        assert "mypkg.legacy" in str(caught[0].message)
        assert "2.0.0" in str(caught[0].message)
        assert "mypkg.modern" in str(caught[0].message)

    def test_custom_message(self) -> None:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            deprecated_module("legacy", message="legacy is gone soon")
        assert str(caught[0].message) == "legacy is gone soon"
