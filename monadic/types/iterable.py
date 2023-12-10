from typing import Callable, TypeVar, Union
import typing
from abc import ABC, abstractmethod
import functools

from .monad import Monad


T = TypeVar('T')
U = TypeVar('U')


class Iterable(typing.Iterable, Monad[T], ABC):
    @classmethod
    @abstractmethod
    def unit(cls, value: T) -> 'Iterable[T]':
        ...

    @classmethod
    @abstractmethod
    def from_iterable(cls, iterable: typing.Iterable):
        return ...

    @classmethod
    @abstractmethod
    def empty(cls) -> 'Iterable':
        ...

    def bind(self, f: Callable[[T], 'Iterable[U]']) -> 'Iterable[U]':
        return functools.reduce(self.__class__.concat, map(f, self), self.empty())  # type: ignore

    @abstractmethod
    def concat(self, other: 'Iterable[U]') -> 'Iterable[Union[T, U]]':
        ...


def take(n: int) -> Callable[[Iterable[T]], Iterable[U]]:
    return lambda iterable: iterable.from_iterable(item for _, item in zip(range(n), iterable))


def fold(f: Callable[[T, T], T]) -> Callable[[Iterable[T]], T]:
    return functools.partial(functools.reduce, f)
