"""Decorator and utilities for deprecating functions, parameters, and classes with zero boilerplate."""

from __future__ import annotations

import functools
import warnings
from typing import Any, Callable, TypeVar

__all__ = [
    "deprecated",
    "deprecated_class",
    "deprecated_module",
    "deprecated_param",
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
