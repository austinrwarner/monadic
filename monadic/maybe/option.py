from typing import Callable, TypeVar
from abc import ABC

from .core import Maybe


T = TypeVar('T')
U = TypeVar('U')


class Option(Maybe[T], ABC):
    @classmethod
    def unit(cls, value: T) -> 'Some[T]':
        return Some(value)

    def _bind(self, f: Callable[[T], 'Option[U]']) -> 'Option[U]':  # type: ignore[override]
        if isinstance(self, Some):
            return f(self.value)
        else:
            return Nothing()


class Some(Option[T]):
    value: T

    def __init__(self, value: T):
        self.value = value

    def __repr__(self):
        return f'Some({repr(self.value)})'

    def __bool__(self):
        return True


class Nothing(Option):
    def __repr__(self):
        return 'Nothing()'

    def __bool__(self):
        return False
