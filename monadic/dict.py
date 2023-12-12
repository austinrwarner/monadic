from typing import TypeVar, Union, Tuple, Callable, Hashable
import typing

from .interfaces import Iterable
from .set import Set
from .list import List
from .option import Some, Nothing, Option

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")

K2 = TypeVar("K2", bound=Hashable)
V2 = TypeVar("V2")


class Dict(Iterable[Tuple[K, V]]):
    inner: typing.Dict[K, V]

    def __init__(
            self,
            inner: Union[
                typing.Iterable[Tuple[K, V]],
                typing.Dict[K, V]
            ]
    ):
        self.inner = dict(inner)

    @classmethod
    def from_iterable(
            cls,
            iterable: typing.Iterable[Tuple[K2, V2]]
    ) -> "Dict[K2, V2]":
        return Dict(iterable)

    @classmethod
    def unit(  # type: ignore[override]
            cls,
            value: Tuple[K2, V2]
    ) -> "Dict[K2, V2]":
        return cls.from_iterable((value,))

    def bind(  # type: ignore[override]
        self, f: Callable[[Tuple[K, V]], "Dict[K2, V2]"]
    ) -> "Dict[K2, V2]":
        return Dict.from_iterable(
            fx for x in self for fx in f(x)
        )

    def apply(  # type: ignore[override]
            self,
            f: "Dict[K, Callable[[Tuple[K, V]], Tuple[K2, V2]]]"
    ) -> "Dict[Union[K, K2], Union[V, V2]]":
        return self.from_iterable(
            f.get(k).default(lambda x: x).unwrap()((k, v)) for k, v in self
        )

    def apply_keys(
            self,
            f: "Dict[K, Callable[[K], K2]]"
    ) -> "Dict[Union[K, K2], V]":
        def accept_tuple(v):
            return lambda x: (v(x[0]), x[1])

        return self.apply(
            Dict.from_iterable(
                (k, accept_tuple(v))
                for k, v in f
            )
        )

    def apply_values(
            self,
            f: "Dict[K, Callable[[V], V2]]"
    ) -> "Dict[K, Union[V, V2]]":
        def accept_tuple(v):
            return lambda x: (x[0], v(x[1]))

        return self.apply(
            Dict.from_iterable(
                (k, accept_tuple(v))
                for k, v in f
            )
        )

    def map(  # type: ignore[override]
            self,
            f: Callable[[Tuple[K, V]], Tuple[K2, V2]]
    ) -> "Dict[K2, V2]":
        return self.from_iterable((f((k, v)) for k, v in self))

    def map_keys(
            self,
            f: Callable[[K], K2]
    ) -> "Dict[K2, V]":
        return self.map(lambda x: (f(x[0]), x[1]))

    def map_values(
            self,
            f: Callable[[V], V2]
    ) -> "Dict[K, V2]":
        return self.map(lambda x: (x[0], f(x[1])))

    @classmethod
    def empty(cls) -> "Dict":
        return cls.from_iterable([])

    def __repr__(self):
        return f"Dict({self.inner})"

    def concat(  # type: ignore[override]
            self,
            other: "Iterable[Tuple[K2, V2]]"
    ) -> "Dict[Union[K, K2], Union[V, V2]]":
        return super().concat(other)  # type: ignore[return-value]

    def filter(  # type: ignore[override]
            self,
            f: Callable[[Tuple[K, V]], bool]
    ) -> "Dict[K, V]":
        return self.from_iterable(filter(f, self))

    def filter_keys(
            self,
            f: Callable[[K], bool]
    ) -> "Dict[K, V]":
        return self.filter(lambda x: f(x[0]))

    def filter_values(
            self,
            f: Callable[[V], bool]
    ) -> "Dict[K, V]":
        return self.filter(lambda x: f(x[1]))

    def __iter__(self):
        return self.inner.items().__iter__()

    def keys(self) -> Set[K]:
        return Set.from_iterable(self.inner.keys())

    def values(self) -> List[V]:
        return List.from_iterable(self.inner.values())

    def get(self, key: K) -> Option[V]:
        try:
            return Some(self.inner[key])
        except KeyError:
            return Nothing()

    def set(
            self,
            key: K2,
            value: V2
    ) -> "Dict[Union[K, K2], Union[V, V2]]":
        return self.append((key, value))  # type: ignore[return-value]

    def __eq__(self, other):
        return isinstance(other, Dict) and self.inner == other.inner
