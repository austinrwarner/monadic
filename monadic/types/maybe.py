from typing import Callable, TypeVar, Union
from abc import ABC, abstractmethod

from .monad import Monad


T = TypeVar('T')
U = TypeVar('U')


class Maybe(Monad[T], ABC):
    def unwrap(self: 'Maybe[T]', default: U) -> 'Maybe[Union[T, U]]':
        return self or self.unit(default)

    @abstractmethod
    def __bool__(self):
        ...


def then(f: Callable[[T], U]) -> Callable[[Maybe[T]], Maybe[U]]:
    return lambda x: x.map(f)


def unwrap(value: T) -> Callable[[Maybe], Maybe[T]]:
    return lambda m: m.unwrap(value)
