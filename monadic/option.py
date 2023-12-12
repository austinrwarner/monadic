from typing import Callable, TypeVar
from abc import ABC, abstractmethod

from .types.maybe import Maybe, UnwrapError


T = TypeVar("T")
U = TypeVar("U")


class Option(Maybe[T], ABC):
    """Monadic type representing a value that may or may not exist.

    This class is a subclass of :class:`Maybe` that implements the
    :class:`Monad` interface. It is a wrapper type that represents a
    value that may or may not exist. It has two subclasses:
    - :class:`Some`
    - :class:`Nothing`
    """
    @classmethod
    def unit(cls, value: T) -> "Some[T]":  # type: ignore[override]
        """Wrap a value in a :class:`Some` instance.

        Parameters
        ----------
        value : T
            The value to wrap.

        Returns
        -------
        Some[T]
            The wrapped value.
        """
        return Some(value)

    @abstractmethod
    def bind(  # type: ignore[override]
            self,
            f: Callable[[T], "Option[U]"]
    ) -> "Option[U]":
        """Chain a function that maps a value to an :class:`Option`.

        If :code:`self` is a :class:`Some`, apply the function to the
        wrapped value. Otherwise (:code:`self` is a :class:`Nothing`),
        return :code:`self`.

        Parameters
        ----------
        f : Callable[[T], Option[U]]
            A function that maps a value to an :class:`Option`.

        Returns
        -------
        Option[U]
            The result of applying the function to the wrapped value.
        """
        ...  # pragma: nocover

    def apply(  # type: ignore[override]
            self,
            f: "Option[Callable[[T], U]]"
    ) -> "Option[U]":
        """Apply a function wrapped in an :class:`Option`.

        If :code:`self` and :code:`f` are both :class:`Some` instances,
        apply the function to the wrapped value and wrap in a :class:`Some`.
        Otherwise, return :class:`Nothing`.

        Parameters
        ----------
        f : Option[Callable[[T], U]]
            A function wrapped in an :class:`Option`.

        Returns
        -------
        Option[U]
            The result of applying the function to the wrapped value.
        """
        if isinstance(f, Some):
            return self.map(f.value)
        else:
            return Nothing()

    @abstractmethod
    def map(  # type: ignore[override]
            self,
            f: Callable[[T], U]
    ) -> "Option[U]":
        """Map a function over the wrapped value.

        If :code:`self` is a :class:`Some`, apply the function to the
        wrapped value and wrap in a :class:`Some`. Otherwise
        (:code:`self` is a :class:`Nothing`), return :class:`Nothing`.

        Parameters
        ----------
        f : Callable[[T], U]
            A function that maps a value to another value.

        Returns
        -------
        Option[U]
            The result of applying the function to the wrapped value.
        """
        ...  # pragma: nocover

    @abstractmethod
    def __eq__(self, other):
        ...  # pragma: nocover


class Some(Option[T]):
    """Option type representing a value that exists.

    This class is a subclass of :class:`Option` that represents a value
    that exists. It has a :code:`value` attribute that contains the
    wrapped value. :code:`Some` instances are truthy.
    """
    value: T

    def __init__(self, value: T):
        self.value = value

    def bind(  # type: ignore[override]
            self,
            f: Callable[[T], Option[U]]
    ) -> Option[U]:
        return f(self.value)

    def map(  # type: ignore[override]
            self,
            f: Callable[[T], U]
    ) -> "Some[U]":
        return Some(f(self.value))

    def unwrap(self) -> T:
        return self.value

    def __repr__(self):
        return f"Some({repr(self.value)})"

    def __bool__(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Some) and other.value == self.value


class Nothing(Option):
    """Option type representing a value that does not exist.

    This class is a subclass of :class:`Option` that represents a value
    that does not exist. :code:`Nothing` instances are falsy.
    """
    def bind(  # type: ignore[override]
            self,
            f: Callable[[T], Option[U]]
    ) -> Option[U]:
        return self

    def map(  # type: ignore[override]
            self,
            f: Callable[[T], U]
    ) -> "Nothing":
        return self

    def unwrap(self):
        raise UnwrapError('Cannot unwrap "Nothing"')

    def __repr__(self):
        return "Nothing()"

    def __bool__(self):
        return False

    def __eq__(self, other):
        return isinstance(other, Nothing)
