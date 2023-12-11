from typing import TypeVar, Union
from abc import ABC, abstractmethod

from .monad import Monad


T = TypeVar("T")
U = TypeVar("U")


class UnwrapError(Exception):
    pass


class Maybe(Monad[T], ABC):
    @classmethod
    @abstractmethod
    def unit(cls, value: U) -> "Maybe[U]":
        ...

    def default(self, value: U) -> "Union[Maybe[T], Maybe[U]]":
        return self or self.unit(value)  # type: ignore[arg-type]

    @abstractmethod
    def unwrap(self) -> T:
        ...

    @abstractmethod
    def __bool__(self):
        ...
