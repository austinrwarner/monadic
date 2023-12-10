from typing import Callable, TypeVar, Generic, Any, overload, Union, Optional
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
    def _bind(self, f: Callable[[T], 'Monad[U]']) -> 'Monad[U]':
        ...

    @classmethod
    @overload
    def bind(cls, f: Callable[[T], 'Monad[U]'], m: 'Monad[T]') -> 'Monad[U]':
        ...

    @classmethod
    @overload
    def bind(cls, f: Callable[[T], 'Monad[U]'], m: None) -> Callable[['Monad[T]'], 'Monad[U]']:
        ...

    @classmethod
    @overload
    def bind(cls, f: Callable[[T], 'Monad[U]']) -> Callable[['Monad[T]'], 'Monad[U]']:
        ...

    @classmethod
    def bind(
            cls,
            f: Callable[[T], 'Monad[U]'],
            m: Optional['Monad[T]'] = None
    ) -> Union[Callable[['Monad[T]'], 'Monad[U]'], 'Monad[U]']:
        if m is None:
            return lambda mm: mm.bind(f, mm)
        else:
            return m._bind(f)

    def _apply(self, f: 'Monad[Callable[[T], U]]') -> 'Monad[U]':
        return Monad.bind(
            lambda ff: Monad.bind(lambda x: self.unit(ff(x)), self),
            f
        )

    @classmethod
    @overload
    def apply(cls, f: 'Monad[Callable[[T], U]]', m: 'Monad[T]') -> 'Monad[U]':
        ...

    @classmethod
    @overload
    def apply(cls, f: 'Monad[Callable[[T], U]]', m: None) -> Callable[['Monad[T]'], 'Monad[U]']:
        ...

    @classmethod
    @overload
    def apply(cls, f: 'Monad[Callable[[T], U]]') -> Callable[['Monad[T]'], 'Monad[U]']:
        ...

    @classmethod
    def apply(
            cls,
            f: 'Monad[Callable[[T], U]]',
            m: Optional['Monad[T]'] = None
    ) -> Union[Callable[['Monad[T]'], 'Monad[U]'], 'Monad[U]']:
        if m is None:
            return lambda mm: mm.apply(f, mm)
        else:
            return m._apply(f)

    def _map(self, f: Callable[[T], U]) -> 'Monad[U]':
        return self.apply(self.unit(f), self)  # type: ignore

    @classmethod
    @overload
    def map(cls, f: Callable[[T], U], m: 'Monad[T]') -> 'Monad[U]':
        ...

    @classmethod
    @overload
    def map(cls, f: Callable[[T], U], m: None) -> Callable[['Monad[T]'], 'Monad[U]']:
        ...

    @classmethod
    @overload
    def map(cls, f: Callable[[T], U]) -> Callable[['Monad[T]'], 'Monad[U]']:
        ...

    @classmethod
    def map(
            cls,
            f: Callable[[T], U],
            m: Optional['Monad[T]'] = None
    ) -> Union['Monad[U]', Callable[['Monad[T]'], 'Monad[U]']]:
        if m is None:
            return lambda mm: mm.map(f, mm)
        else:
            return m._map(f)
        
    def __rshift__(self, other: Callable[['Monad[T]'], 'Monad[U]']) -> 'Monad[U]':
        if not callable(other):
            raise TypeError(f'Cannot pipe {self} into {other}')

        return other(self)
