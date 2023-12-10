from typing import TypeVar, Union
import typing

from .types.iterable import Iterable


T = TypeVar('T')
U = TypeVar('U')


class Set(Iterable[T]):
    inner: set[T]

    def __init__(self, inner: typing.Iterable[T]):
        self.inner = set(inner)

    @classmethod
    def from_iterable(cls, iterable: typing.Iterable):
        return Set(iterable)

    @classmethod
    def unit(cls, value: T) -> 'Set[T]':
        return cls({value})

    @classmethod
    def empty(cls) -> 'Set':
        return cls(set())

    def __repr__(self):
        return f'Set({self.inner})'

    def concat(self: 'Set[T]', other: 'Set[U]') -> 'Set[Union[T, U]]':
        return Set(self.inner | other.inner)

    def __iter__(self):
        return self.inner.__iter__()
