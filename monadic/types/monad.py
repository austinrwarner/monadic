from typing import Callable, TypeVar, Generic
from abc import ABC, abstractmethod
import sys

if sys.version_info <= (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec


P = ParamSpec('P')
R = TypeVar('R')

T = TypeVar('T')
U = TypeVar('U')


class Monad(ABC, Generic[T]):
    @classmethod
    @abstractmethod
    def unit(cls, value: U) -> 'Monad[U]':
        ...

    @abstractmethod
    def bind(self, f: Callable[[T], 'Monad[U]']) -> 'Monad[U]':
        ...

    def apply(self, f: 'Monad[Callable[[T], U]]') -> 'Monad[U]':
        return f.bind(
            lambda ff: self.bind(
                lambda x: self.unit(ff(x))
            )
        )

    def map(self, f: Callable[[T], U]) -> 'Monad[U]':
        return self.apply(self.unit(f))
