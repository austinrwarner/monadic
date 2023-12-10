from typing import TypeVar, Union
import typing

from .types.iterable import Iterable


T = TypeVar("T")
U = TypeVar("U")


class List(Iterable[T]):
    inner: typing.List[T]

    def __init__(self, inner: typing.Iterable[T]):
        self.inner = list(inner)

    @classmethod
    def from_iterable(cls, iterable: typing.Iterable):
        return List(iterable)

    @classmethod
    def unit(cls, value: T) -> "List[T]":  # type: ignore[override]
        return cls([value])

    @classmethod
    def empty(cls) -> "List":
        return cls([])

    def __repr__(self):
        return f"List({self.inner})"

    def concat(self, other: "Iterable[U]") -> "List[Union[T, U]]":
        if isinstance(other, List):
            return List(self.inner + other.inner)
        else:
            return super().concat(other)  # type: ignore[return-value]

    def __iter__(self):
        return self.inner.__iter__()
