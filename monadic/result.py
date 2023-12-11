from typing import Callable, TypeVar, Tuple, Type
from abc import ABC

from .types.maybe import Maybe, UnwrapError


T = TypeVar("T")
U = TypeVar("U")


class UnspecifiedException(Exception):
    def __repr__(self):
        return ''


class Result(Maybe[T], ABC):
    @classmethod
    def unit(cls, value: T) -> "Ok[T]":  # type: ignore[override]
        return Ok(value)

    def map(  # type: ignore[override]
            self,
            f: Callable[[T], U]
    ) -> "Result[U]":
        def _wrap_exception(t: T) -> Result[U]:
            try:
                return Ok(f(t))
            except Exception as e:
                return Error(e)

        return self.bind(_wrap_exception)  # type: ignore[return-value]

    @staticmethod
    def attempt(
            __f: Callable[..., T],
            __catch: Tuple[Type[Exception], ...],
            *args,
            **kwargs
    ) -> "Result[T]":
        try:
            return Ok(__f(*args, **kwargs))
        except __catch as e:
            return Error(e)


class Ok(Result[T]):
    value: T

    def __init__(self, value: T):
        self.value = value

    def bind(  # type: ignore[override]
            self,
            f: Callable[[T], "Result[U]"]
    ) -> "Result[U]":
        return f(self.value)

    def unwrap(self) -> T:
        return self.value

    def __repr__(self):
        return f"Ok({repr(self.value)})"

    def __bool__(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Ok) and self.value == other.value


class Error(Result):
    exception: Exception

    def __init__(self, exception: Exception = UnspecifiedException()):
        self.exception = exception

    def bind(  # type: ignore[override]
            self,
            f: Callable[[T], "Result[U]"]
    ) -> "Result[U]":
        return self

    def unwrap(self):
        raise UnwrapError('Cannot unwrap "Error"') from self.exception

    def __repr__(self):
        return f"Error({repr(self.exception)})"

    def __bool__(self):
        return False
