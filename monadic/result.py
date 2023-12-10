from typing import Callable, TypeVar
from abc import ABC

from .types.maybe import Maybe


T = TypeVar("T")
U = TypeVar("U")


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


class Error(Result):
    exception: Exception

    def __init__(self, exception: Exception):
        self.exception = exception

    def bind(  # type: ignore[override]
            self,
            f: Callable[[T], "Result[U]"]
    ) -> "Result[U]":
        return self

    def unwrap(self):
        raise ValueError('Cannot unwrap "Error"') from self.exception

    def __repr__(self):
        return f"Error({repr(self.exception)})"

    def __bool__(self):
        return False
