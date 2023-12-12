from typing import TypeVar, Union, Callable
import typing

from .interfaces import Iterable


T = TypeVar("T")
U = TypeVar("U")


class List(Iterable[T]):
    """A monadic list.

    This is a wrapper around the built-in list type that implements the
    :class:`Iterable` interface. Following a functional style, it is
    immutable. To add items to the end of the list, use the :meth:`append`
    or :meth:`concat`.

    Parameters
    ----------
    inner : typing.Iterable[T]
        The iterable to wrap as a list.


    Examples
    --------
    >>> from monadic.list import List
    >>> List([1, 2, 3]).map(lambda x: x + 1)
    List([2, 3, 4])
    >>> List([1, 2, 3]).bind(lambda x: List([x, x + 1]))
    List([1, 2, 2, 3, 3, 4])
    >>> List([1, 2, 3]).apply(List([str, float]))
    List(['1', 2.0])
    >>> List([1, 2, 3]).concat([4, 5, 6])
    List([1, 2, 3, 4, 5, 6])
    >>> List([1, 2, 3]).append(4)
    List([1, 2, 3, 4])
    >>> list(List([1, 2, 3]))
    [1, 2, 3]
    """
    _inner: typing.List[T]

    def __init__(self, inner: typing.Iterable[T]):
        self._inner = list(inner)

    @classmethod
    def from_iterable(cls, iterable: typing.Iterable[U]) -> "List[U]":
        return List(iterable)

    @classmethod
    def unit(cls, value: T) -> "List[T]":  # type: ignore[override]
        """Wrap a single value in a :class:`List`.

        Parameters
        ----------
        value : T
            The value to wrap.

        Returns
        -------
        List[T]
            A new list containing the value.
        """
        return cls([value])

    @classmethod
    def empty(cls) -> "List":
        return cls([])

    def bind(  # type: ignore[override]
            self,
            f: Callable[[T], Iterable[U]]
    ) -> "List[U]":
        """Chain a function that maps a value to a :class:`List`.

        Parameters
        ----------
        f : Callable[[T], List[U]]
            A function that maps a value to a :class:`List`.

        Returns
        -------
        List[U]
            The result of applying the function to each element of the list,
            and concatenating the results.
        """
        return List.from_iterable(fx for x in self for fx in f(x))

    def apply(  # type: ignore[override]
            self,
            f: Iterable[Callable[[T], U]]
    ) -> "List[U]":
        """Apply each function in a list to each element of a list.

        Parameters
        ----------
        f : List[Callable[[T], U]]
            A list of functions.

        Returns
        -------
        List[U]
            A new list containing the results of applying each function to
            each element of the original list.
        """
        return super().apply(f)  # type: ignore[return-value]

    def map(  # type: ignore[override]
            self,
            f: Callable[[T], U]
    ) -> "List[U]":
        """Map a function over a list.

        Parameters
        ----------
        f : Callable[[T], U]
            A function that maps a value to a new value.

        Returns
        -------
        List[U]
            A new list containing the results of applying the function to
            each element of the original list.
        """
        return List.from_iterable(map(f, self))

    def zip_apply(
            self,
            f: typing.Iterable[Callable[[T], U]]
    ) -> "List[U]":
        """Apply each function in an iterable to the corresponding element.

        Parameters
        ----------
        f : Iterable[Callable[[T], U]]
            An iterable of functions.

        Returns
        -------
        List[U]
            A new list containing the results of applying each function to
            the corresponding element of the original list.
        """
        return List.from_iterable(fx(x) for x, fx in zip(self, f))

    def __repr__(self):
        return f"List({self._inner})"

    def concat(self, other: typing.Iterable[U]) -> "List[Union[T, U]]":
        return List(self._inner + list(other))

    def __iter__(self):
        return self._inner.__iter__()

    def __eq__(self, other):
        return isinstance(other, List) and self._inner == other._inner
