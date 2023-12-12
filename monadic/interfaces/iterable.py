from typing import Callable, TypeVar, Union, Optional
import typing
from abc import ABC, abstractmethod
import functools
import itertools

from .monad import Monad


T = TypeVar("T")
U = TypeVar("U")


class Iterable(typing.Iterable, Monad[T], ABC):
    """Iterable monad interface.

    Base class for monads that represent a collection of values that
    may be iterated over. Subclasses must implement the following methods:

    - :code:`unit` (a class method)
        This method is a constructor that wraps a single valid value
    - :code:`bind` (an instance method)
        How to apply a function to a value that may or may not exist.
    - :code:`from_iterable` (a class method)
        Wrap an iterable in the monad class.
    - :code:`empty` (a class method)
        Create an empty monad.
    - :code:`__eq__` (an instance method)
        Compare two monads for equality.

    :code:`monadic.Iterable` instances are also Python iterables, so
    they can be used in for loops and comprehensions.
    """

    @classmethod
    @abstractmethod
    def unit(cls, value: U) -> "Iterable[U]":
        """Wrap a value in the monad class.

        Parameters
        ----------
        value : U
            The value to wrap.

        Returns
        -------
        Iterable[U]
            The wrapped value.
        """
        ...  # pragma: no cover

    @classmethod
    @abstractmethod
    def from_iterable(cls, iterable: typing.Iterable[U]) -> "Iterable[U]":
        """Wrap an iterable in a monad.

        Parameters
        ----------
        iterable : typing.Iterable
            The iterable to wrap.

        Returns
        -------
        Iterable
            A new monad containing the contents of the iterable.
        """
        ...  # pragma: no cover

    @classmethod
    def empty(cls) -> "Iterable":
        """Create an empty monad."""
        return cls.from_iterable([])

    def bind(  # type: ignore[override]
        self, f: Callable[[T], "Iterable[U]"]
    ) -> "Iterable[U]":
        """Chain a function that maps a value to an Iterable.

        Parameters
        ----------
        f : Callable[[T], Iterable[U]]
            A function that maps a value to an Iterable.

        Returns
        -------
        Iterable[U]
            The result of applying the function to each value in the
            Iterable and concatenating the results.
        """
        return functools.reduce(
            self.__class__.concat,  # type: ignore[arg-type]
            map(f, self),
            self.empty()
        )

    def apply(  # type: ignore[override]
            self,
            f: "Iterable[Callable[[T], U]]"
    ) -> "Iterable[U]":
        """Apply an iterable of functions to an iterable.

        Parameters
        ----------
        f : Iterable[Callable[[T], U]]
            An iterable of functions.

        Returns
        -------
        Iterable[U]
            The result of applying each function to each value in the
            iterable and concatenating the results.
        """
        return self.bind(lambda x: f.map(lambda g: g(x)))

    def map(  # type: ignore[override]
        self, f: Callable[[T], U]
    ) -> "Iterable[U]":
        """Map a function over an iterable.

        Parameters
        ----------
        f : Callable[[T], U]
            A function to map over the iterable.

        Returns
        -------
        Iterable[U]
            A new iterable containing the result of applying the function
            to each value in the iterable.
        """
        return self.from_iterable(map(f, self))

    def concat(self, other: typing.Iterable[U]) -> "Iterable[Union[T, U]]":
        """Add the contents of another iterable to this iterable.

        Parameters
        ----------
        other : typing.Iterable[U]
            The iterable to add.

        Returns
        -------
        Iterable[Union[T, U]]
            A new iterable containing the contents of both iterables.
        """
        return self.from_iterable(itertools.chain(self, other))

    def append(self, value: U) -> "Iterable[Union[T, U]]":
        """Add a value to this iterable.

        Parameters
        ----------
        value : U
            The value to add.

        Returns
        -------
        Iterable[Union[T, U]]
            A new iterable containing the old contents and the value.
        """
        return self.concat(self.unit(value))

    def filter(self, f: Callable[[T], bool]) -> "Iterable[T]":
        """Filter the values in this iterable.

        Parameters
        ----------
        f : Callable[[T], bool]
            A function that returns True for values to keep.

        Returns
        -------
        Iterable[T]
            A new iterable containing only the values that pass the filter.
        """
        return self.from_iterable(filter(f, self))

    def take(self, n: int) -> "Iterable[T]":
        """Take the first n values from this iterable.

        Parameters
        ----------
        n : int
            The number of values to take.

        Returns
        -------
        Iterable[T]
            A new iterable containing the first n values.
        """
        return self.from_iterable(itertools.islice(self, n))

    def fold(
            self,
            f: Callable[[U, T], U],
            initial: Optional[U] = None
    ) -> U:
        """Fold the values in this iterable.

        Parameters
        ----------
        f : Callable[[U, T], U]
            A function that takes the current value and the next value
            and returns the new value.
        initial : Optional[U]
            The initial value to use. If not provided, the first value
            in the iterable is used.

        Returns
        -------
        U
            The result of folding the iterable.
        """
        if initial is not None:
            return functools.reduce(f, self, initial)
        else:
            return functools.reduce(f, self)

    @abstractmethod
    def __eq__(self, other):
        ...  # pragma: no cover
