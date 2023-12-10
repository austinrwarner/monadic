from typing import Callable, TypeVar, Generic, overload, Union, Optional
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
    def unit(cls, value: T) -> 'Monad[T]':
        ...

    @abstractmethod
    def bind(self, f: Callable[[T], 'Monad[U]']) -> 'Monad[U]':
        ...

    def apply(self, f: 'Monad[Callable[[T], U]]') -> 'Monad[U]':
        return f.bind(
            lambda ff: self.bind(lambda x: self.unit(ff(x)))
        )

    def map(self, f: Callable[[T], U]) -> 'Monad[U]':
        return self.apply(self.unit(f))
        
    def __rshift__(self, other: Callable[['Monad[T]'], 'Monad[U]']) -> 'Monad[U]':
        if not callable(other):
            raise TypeError(f'Cannot pipe {self} into {other}')

        return other(self)
