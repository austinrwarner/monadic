from typing import TypeVar, Callable

from monadic import Monad


T = TypeVar('T')


class SimpleMonad(Monad[T]):
    value: T

    def __init__(self, value: T):
        self.value = value

    @classmethod
    def unit(cls, value: T) -> 'SimpleMonad[T]':
        return cls(value)

    def bind(self, f: Callable[[T], 'SimpleMonad[T]']) -> 'SimpleMonad[T]':
        return f(self.value)


def test_unit():
    assert SimpleMonad.unit(1).value == 1


def test_bind():
    assert SimpleMonad.unit(1).bind(lambda x: SimpleMonad.unit(x + 1)).value == 2


def test_apply():
    assert SimpleMonad.unit(1).apply(SimpleMonad.unit(lambda x: x + 1)).value == 2


def test_map():
    assert SimpleMonad.unit(1).map(lambda x: x + 1).value == 2
