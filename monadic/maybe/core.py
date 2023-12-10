from typing import Callable, TypeVar, Union
from abc import ABC, abstractmethod

from ..monad import Monad


T = TypeVar('T')
U = TypeVar('U')


class Maybe(Monad[T], ABC):
    def default(self: 'Maybe[T]', value: U) -> 'Maybe[Union[T, U]]':
        return self or self.unit(value)

    @abstractmethod
    def __bool__(self):
        ...


def then(f: Callable[[T], U]) -> Callable[[Maybe[T]], Maybe[U]]:
    return Maybe.map(f)  # type: ignore[return-value]


def default(value: T) -> Callable[[Maybe], Maybe[T]]:
    return lambda m: m.default(value)
