"""Decorator and utilities for deprecating functions, parameters, and classes with zero boilerplate."""

from __future__ import annotations

import contextlib
import functools
import warnings
from collections.abc import Iterator
from typing import Any, Callable, TypeVar

__all__ = [
    "deprecated",
    "deprecated_attribute",
    "deprecated_class",
    "deprecated_module",
    "deprecated_param",
    "silenced",
]

F = TypeVar("F", bound=Callable[..., Any])
C = TypeVar("C", bound=type)


def deprecated(
    remove_in: str = "",
    *,
    alternative: str = "",
    message: str = "",
) -> Callable[[F], F]:
    """Mark a function as deprecated.

    Args:
        remove_in: Version when the function will be removed (e.g. ``"2.0.0"``).
        alternative: Suggested replacement function or approach.
        message: Custom deprecation message. Overrides the auto-generated one.
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            msg = _build_message(
                kind="Function",
                name=func.__qualname__,
                remove_in=remove_in,
                alternative=alternative,
                message=message,
            )
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


def deprecated_param(
    param: str,
    *,
    renamed_to: str = "",
    remove_in: str = "",
) -> Callable[[F], F]:
    """Warn when a deprecated parameter is used.

    If *renamed_to* is provided, the old parameter value is automatically
    forwarded to the new name so callers can migrate gradually.

    Args:
        param: Name of the deprecated parameter.
        renamed_to: New parameter name the old one maps to.
        remove_in: Version when the parameter will be removed.
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if param in kwargs:
                parts: list[str] = [
                    f"Parameter '{param}' of {func.__qualname__}() is deprecated."
                ]
                if renamed_to:
                    parts.append(f"Use '{renamed_to}' instead.")
                if remove_in:
                    parts.append(f"Will be removed in {remove_in}.")
                warnings.warn(" ".join(parts), DeprecationWarning, stacklevel=2)

                if renamed_to and renamed_to not in kwargs:
                    kwargs[renamed_to] = kwargs.pop(param)

            return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator


def deprecated_class(
    remove_in: str = "",
    *,
    alternative: str = "",
    message: str = "",
) -> Callable[[C], C]:
    """Mark a class as deprecated. Warns on instantiation.

    Args:
        remove_in: Version when the class will be removed.
        alternative: Suggested replacement class or approach.
        message: Custom deprecation message. Overrides the auto-generated one.
    """

    def decorator(cls: C) -> C:
        original_init = cls.__init__

        @functools.wraps(original_init)
        def new_init(self: Any, *args: Any, **kwargs: Any) -> None:
            msg = _build_message(
                kind="Class",
                name=cls.__qualname__,
                remove_in=remove_in,
                alternative=alternative,
                message=message,
            )
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            original_init(self, *args, **kwargs)

        cls.__init__ = new_init  # type: ignore[method-assign]
        return cls

    return decorator


def deprecated_module(
    name: str,
    *,
    remove_in: str = "",
    alternative: str = "",
    message: str = "",
) -> None:
    """Emit a one-time ``DeprecationWarning`` indicating that a module is deprecated.

    Call this from a deprecated module's ``__init__.py`` so importing the
    module surfaces the warning to consumers.

    Args:
        name: Module name (typically pass ``__name__``).
        remove_in: Version when the module will be removed.
        alternative: Suggested replacement module.
        message: Custom deprecation message. Overrides the auto-generated one.

    Example:
        >>> # in mypkg/legacy/__init__.py
        >>> from philiprehberger_deprecate import deprecated_module
        >>> deprecated_module(__name__, remove_in="2.0.0", alternative="mypkg.modern")
    """
    msg = _build_message(
        kind="Module",
        name=name,
        remove_in=remove_in,
        alternative=alternative,
        message=message,
    )
    warnings.warn(msg, DeprecationWarning, stacklevel=2)


def _build_message(
    *,
    kind: str,
    name: str,
    remove_in: str,
    alternative: str,
    message: str,
) -> str:
    """Build a standardised deprecation warning message."""
    if message:
        return message
    parts: list[str] = [f"{kind} '{name}' is deprecated."]
    if remove_in:
        parts.append(f"Will be removed in {remove_in}.")
    if alternative:
        parts.append(f"Use '{alternative}' instead.")
    return " ".join(parts)


class deprecated_attribute:
    """Descriptor that emits ``DeprecationWarning`` when the attribute is accessed.

    Args:
        name: Name of the deprecated attribute (used in the warning message).
        since: Version in which the attribute was deprecated.
        removed_in: Version when the attribute will be removed.
        replacement: Name of the replacement attribute on the same instance.
            When set, reading the deprecated attribute returns the replacement's
            value transparently.

    Example:
        >>> class Foo:
        ...     old_value = deprecated_attribute(
        ...         "old_value",
        ...         since="1.0",
        ...         removed_in="2.0",
        ...         replacement="new_value",
        ...     )
        ...     new_value = 42
    """

    def __init__(
        self,
        name: str,
        *,
        since: str | None = None,
        removed_in: str | None = None,
        replacement: str | None = None,
    ) -> None:
        self._name = name
        self._since = since
        self._removed_in = removed_in
        self._replacement = replacement
        self._attr_name = name

    def __set_name__(self, owner: type, attr_name: str) -> None:
        self._attr_name = attr_name

    def _warn(self) -> None:
        parts: list[str] = [f"Attribute '{self._name}' is deprecated."]
        if self._since:
            parts.append(f"Deprecated since {self._since}.")
        if self._removed_in:
            parts.append(f"Will be removed in {self._removed_in}.")
        if self._replacement:
            parts.append(f"Use '{self._replacement}' instead.")
        warnings.warn(" ".join(parts), DeprecationWarning, stacklevel=3)

    def __get__(self, instance: Any, owner: type) -> Any:
        if instance is None:
            return self
        self._warn()
        if self._replacement is not None and hasattr(instance, self._replacement):
            return getattr(instance, self._replacement)
        return instance.__dict__.get(f"_{self._attr_name}")

    def __set__(self, instance: Any, value: Any) -> None:
        self._warn()
        instance.__dict__[f"_{self._attr_name}"] = value


@contextlib.contextmanager
def silenced() -> Iterator[None]:
    """Context manager suppressing ``DeprecationWarning`` emitted by this package.

    Useful in tests that intentionally exercise deprecated APIs.

    Example:
        >>> with silenced():
        ...     old_function()  # no warning emitted
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        yield
