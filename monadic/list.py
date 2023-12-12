from typing import TypeVar, Union, Callable
import typing

from .interfaces import Iterable


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

    def bind(  # type: ignore[override]
            self,
            f: Callable[[T], "List[U]"]
    ) -> "List[U]":
        return List.from_iterable(fx for x in self for fx in f(x))

    def apply(  # type: ignore[override]
            self,
            f: "List[Callable[[T], U]]"
    ) -> "List[U]":
        return List.from_iterable(f(x) for x, f in zip(self, f))

    def map(  # type: ignore[override]
            self,
            f: Callable[[T], U]
    ) -> "List[U]":
        return List.from_iterable(map(f, self))

    def __repr__(self):
        return f"List({self.inner})"

    def concat(self, other: "Iterable[U]") -> "List[Union[T, U]]":
        if isinstance(other, List):
            return List(self.inner + other.inner)
        else:
            return super().concat(other)  # type: ignore[return-value]

    def __iter__(self):
        return self.inner.__iter__()

    def __eq__(self, other):
        return isinstance(other, List) and self.inner == other.inner
