from typing import Callable, TypeVar
from abc import ABC, abstractmethod

from .types.maybe import Maybe, UnwrapError


T = TypeVar("T")
U = TypeVar("U")


class Option(Maybe[T], ABC):
    @classmethod
    def unit(cls, value: T) -> "Some[T]":  # type: ignore[override]
        return Some(value)

    @abstractmethod
    def bind(  # type: ignore[override]
            self,
            f: Callable[[T], "Option[U]"]
    ) -> "Option[U]":
        ...  # pragma: nocover

    def apply(  # type: ignore[override]
            self,
            f: "Option[Callable[[T], U]]"
    ) -> "Option[U]":
        if isinstance(f, Some):
            return self.map(f.value)
        else:
            return Nothing()

    @abstractmethod
    def map(  # type: ignore[override]
            self,
            f: Callable[[T], U]
    ) -> "Option[U]":
        ...  # pragma: nocover

    @abstractmethod
    def __eq__(self, other):
        ...  # pragma: nocover


class Some(Option[T]):
    value: T

    def __init__(self, value: T):
        self.value = value

    def bind(  # type: ignore[override]
            self,
            f: Callable[[T], Option[U]]
    ) -> Option[U]:
        return f(self.value)

    def map(  # type: ignore[override]
            self,
            f: Callable[[T], U]
    ) -> "Some[U]":
        return Some(f(self.value))

    def unwrap(self) -> T:
        return self.value

    def __repr__(self):
        return f"Some({repr(self.value)})"

    def __bool__(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Some) and other.value == self.value


class Nothing(Option):
    def bind(  # type: ignore[override]
            self,
            f: Callable[[T], Option[U]]
    ) -> Option[U]:
        return self

    def map(  # type: ignore[override]
            self,
            f: Callable[[T], U]
    ) -> "Nothing":
        return self

    def unwrap(self):
        raise UnwrapError('Cannot unwrap "Nothing"')

    def __repr__(self):
        return "Nothing()"

    def __bool__(self):
        return False

    def __eq__(self, other):
        return isinstance(other, Nothing)
