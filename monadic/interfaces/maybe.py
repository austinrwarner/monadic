from typing import TypeVar, Union
from abc import ABC, abstractmethod

from .monad import Monad


T = TypeVar("T")
U = TypeVar("U")


class UnwrapError(Exception):
    """Raised when attempting to unwrap a value that does not exist."""
    pass


class Maybe(Monad[T], ABC):
    """Maybe monad interface.

    Base class for monads that represent a value that may or may not
    exist. Subclasses must implement the following methods:

    - :code:`unit` (a class method)
        This method is a constructor that wraps a single valid value
    - :code:`bind` (an instance method)
        How to apply a function to a value that may or may not exist.
    - :code:`unwrap` (an instance method)
        Retrieve the wrapped value. If the value does not exist, raise
        an :class:`UnwrapError`
    - :code:`__bool__` (an instance method)
        Return whether the value exists.
    """

    @classmethod
    @abstractmethod
    def unit(cls, value: U) -> "Maybe[U]":
        ...  # pragma: no cover

    def default(self, value: U) -> "Union[Maybe[T], Maybe[U]]":
        """Return a default value if the value does not exist.

        If the value exists, return the wrapped value;
        otherwise, return the wrapped default value.

        Parameters
        ----------
        value : U
            The default value.

        Returns
        -------
        Union[Maybe[T], Maybe[U]]
            The wrapped value or the wrapped default value.
        """
        return self or self.unit(value)  # type: ignore[arg-type]

    @abstractmethod
    def unwrap(self) -> T:
        """
        Retrieve the wrapped value.

        Raises
        ------
        UnwrapError
            If the value does not exist.

        Returns
        -------
        T
            The wrapped value.
        """
        ...  # pragma: no cover

    @abstractmethod
    def __bool__(self):
        ...  # pragma: no cover
