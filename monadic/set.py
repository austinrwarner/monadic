from typing import TypeVar, Union, Callable
import typing

from .types.iterable import Iterable


T = TypeVar("T")
U = TypeVar("U")


class Set(Iterable[T]):
    inner: typing.Set[T]

    def __init__(self, inner: typing.Iterable[T]):
        self.inner = set(inner)

    @classmethod
    def from_iterable(cls, iterable: typing.Iterable):
        return Set(iterable)

    @classmethod
    def unit(cls, value: T) -> "Set[T]":  # type: ignore[override]
        return cls({value})

    @classmethod
    def empty(cls) -> "Set":
        return cls(set())

    def bind(  # type: ignore[override]
            self,
            f: Callable[[T], "Iterable[U]"]
    ) -> "Set[U]":
        return Set.from_iterable(fx for x in self for fx in f(x))

    def apply(  # type: ignore[override]
            self,
            f: "Iterable[Callable[[T], U]]"
    ) -> "Set[U]":
        return Set.from_iterable(f(x) for x, f in zip(self, f))

    def map(  # type: ignore[override]
            self,
            f: Callable[[T], U]
    ) -> "Set[U]":
        return Set.from_iterable(map(f, self))

    def __repr__(self):
        return f"Set({self.inner})"

    def concat(self, other: "Iterable[U]") -> "Set[Union[T, U]]":
        if isinstance(other, Set):
            return Set(self.inner | other.inner)
        else:
            return super().concat(other)  # type: ignore[return-value]

    def __iter__(self):
        return self.inner.__iter__()

    def __eq__(self, other):
        return isinstance(other, Set) and self.inner == other.inner
