from typing import Callable, TypeVar, Union
import typing
from abc import ABC, abstractmethod
import functools
import itertools

from .monad import Monad


T = TypeVar("T")
U = TypeVar("U")


class Iterable(typing.Iterable, Monad[T], ABC):
    @classmethod
    @abstractmethod
    def unit(cls, value: U) -> "Iterable[U]":
        ...

    @classmethod
    @abstractmethod
    def from_iterable(cls, iterable: typing.Iterable):
        return ...

    @classmethod
    def empty(cls) -> "Iterable":
        return cls.from_iterable([])

    def bind(  # type: ignore[override]
        self, f: Callable[[T], "Iterable[U]"]
    ) -> "Iterable[U]":
        return functools.reduce(
            self.__class__.concat,  # type: ignore[arg-type]
            map(f, self),
            self.empty()
        )

    def concat(self, other: "Iterable[U]") -> "Iterable[Union[T, U]]":
        return self.from_iterable(itertools.chain(self, other))

    def append(self, value: U) -> "Iterable[Union[T, U]]":
        return self.concat(self.unit(value))
