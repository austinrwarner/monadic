from typing import Callable, TypeVar, Any

from .types.monad import Monad


T = TypeVar("T")
U = TypeVar("U")
V = TypeVar("V")


class Lazy(Monad[Callable[[Monad[T]], Monad[U]]]):
    """Lazy monad"""

    func: Callable[[Monad[T]], Monad[U]]

    def __init__(
            self,
            func: Callable[[Monad[T]], Monad[U]] = lambda x: x  # type: ignore
    ) -> None:
        self.func = func

    @classmethod
    def unit(cls, value: Monad[V]) -> "Lazy[Any, V]":  # type: ignore[override]
        return cls(lambda _: value)  # type: ignore

    def bind(  # type: ignore[override]
            self,
            f: Callable[[U], Monad[V]]
    ) -> "Lazy[T, V]":
        return Lazy(lambda x: self(x).bind(f))

    def apply(  # type: ignore[override]
            self,
            f: "Monad[Callable[[U], V]]"
    ) -> "Lazy[T, V]":
        return Lazy(lambda x: (self(x).apply(f)))

    def map(  # type: ignore[override]
            self,
            f: Callable[[U], V]
    ) -> "Lazy[T, V]":
        return Lazy(lambda x: self(x).map(f))

    def __call__(self, value: Monad[T]) -> Monad[U]:
        return self.func(value)
