from typing import Callable, TypeVar
from abc import ABC

from .types.maybe import Maybe


T = TypeVar('T')
U = TypeVar('U')


class Option(Maybe[T], ABC):
    @classmethod
    def unit(cls, value: T) -> 'Some[T]':  # type: ignore[override]
        return Some(value)


class Some(Option[T]):
    value: T

    def __init__(self, value: T):
        self.value = value

    def bind(self, f: Callable[[T], Option[U]]) -> Option[U]:  # type: ignore[override]
        return f(self.value)

    def unwrap(self) -> T:
        return self.value

    def __repr__(self):
        return f'Some({repr(self.value)})'

    def __bool__(self):
        return True


class Nothing(Option):
    def bind(self, f: Callable[[T], Option[U]]) -> Option[U]:  # type: ignore[override]
        return self

    def unwrap(self):
        raise ValueError('Cannot unwrap "Nothing"')

    def __repr__(self):
        return 'Nothing()'

    def __bool__(self):
        return False
