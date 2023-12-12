from typing import TypeVar, Union, Callable
import typing

from .interfaces import Iterable


T = TypeVar("T")
U = TypeVar("U")


class Set(Iterable[T]):
    """A monadic set.

    This is a wrapper around the built-in set type that implements the
    :class:`Iterable` interface. Following a functional style, it is
    immutable. To add items to the set, use :meth:`append` or :meth:`concat`.

    Parameters
    ----------
    inner : typing.Iterable[T]
        The iterable to wrap as a set.

    Examples
    --------
    >>> from monadic.set import Set
    >>> Set({1, 2, 3}).map(lambda x: x + 1)
    Set({2, 3, 4})
    >>> Set({1, 2, 3}).bind(lambda x: Set({x, x + 1}))
    Set({1, 2, 3, 4})
    >>> Set({1, 2, 3}).apply(Set({str, float}))
    Set({1.0, 2.0, 3.0, '2', '1', '3'})
    >>> Set({1, 2, 3}).concat({3, 4, 5})
    Set({1, 2, 3, 4, 5})
    >>> Set({1, 2, 3}).append(4)
    Set({1, 2, 3, 4})
    >>> list(Set({1, 2, 3}))
    [1, 2, 3]
    """
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
            f: Callable[[T], Iterable[U]]
    ) -> "Set[U]":
        """Chain a function that maps a value to an iterable.

        Parameters
        ----------
        f : Callable[[T], Iterable[U]]
            A function that maps a value to an iterable.

        Returns
        -------
        Set[U]
            The result of applying the function to each value in the
            set and concatenating the results.
        """
        return Set.from_iterable(fx for x in self for fx in f(x))

    def apply(  # type: ignore[override]
            self,
            f: Iterable[Callable[[T], U]]
    ) -> "Set[U]":
        """Apply an iterable of functions to a set.

        Parameters
        ----------
        f : Iterable[Callable[[T], U]]
            An iterable of functions.

        Returns
        -------
        Set[U]
            The result of applying each function to each value in the
            set and concatenating the results.
        """
        return super().apply(f)  # type: ignore[return-value]

    def map(  # type: ignore[override]
            self,
            f: Callable[[T], U]
    ) -> "Set[U]":
        """Map a function over a set.

        Parameters
        ----------
        f : Callable[[T], U]
            A function that maps a value to a new value.

        Returns
        -------
        Set[U]
            A new set containing the results of applying the function to
            each value in the original set.
        """
        return Set.from_iterable(map(f, self))

    def __repr__(self):
        return f"Set({self.inner})"

    def concat(self, other: typing.Iterable[U]) -> "Set[Union[T, U]]":
        return Set(self.inner | set(other))

    def __iter__(self):
        return self.inner.__iter__()

    def __eq__(self, other):
        return isinstance(other, Set) and self.inner == other.inner
