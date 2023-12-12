import typing

from monadic.interfaces.iterable import Iterable, U


class GenericIterable(Iterable[U]):
    inner: typing.List[U]

    def __init__(self, inner: typing.Iterable[U]):
        self.inner = list(inner)

    @classmethod
    def unit(cls, value: U) -> "Iterable[U]":
        return cls([value])

    @classmethod
    def from_iterable(cls, iterable: typing.Iterable):
        return cls(iterable)

    def __eq__(self, other):
        return isinstance(other, Iterable) and self.inner == other.inner

    def __iter__(self):
        return self.inner.__iter__()

    def __repr__(self):
        return f"GenericIterable({self.inner})"


def test_bind():
    assert GenericIterable([1, 2, 3]).bind(lambda x: [x, x]) == GenericIterable([1, 1, 2, 2, 3, 3])


def test_apply():
    assert GenericIterable([1, 2, 3]).apply(GenericIterable([str, float])) == GenericIterable(['1', 1.0, '2', 2.0, '3', 3.0])


def test_map():
    assert GenericIterable([1, 2, 3]).map(lambda x: x + 1) == GenericIterable([2, 3, 4])
