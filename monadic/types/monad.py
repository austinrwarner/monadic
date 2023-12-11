from typing import Callable, TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar("T")
U = TypeVar("U")


class Monad(ABC, Generic[T]):
    """Monad interface.

    This is an abstract base class for monads. Monads are wrapper
    types that allow for chaining operations together.

    Subclasses of this class must implement two methods:
    - `unit` (a class method)
        This method is a constructor that wraps a single value
    - `bind` (an instance method)
        This method takes a function that maps a value to a monad
        and returns a monad of the same type.

    The interface is somewhat abstract. See :class:`monadic.option.Option`
    as an example.
    """
    @classmethod
    @abstractmethod
    def unit(cls, value: U) -> "Monad[U]":
        """Wrap a value in the monad class."""
        ...

    @abstractmethod
    def bind(self, f: Callable[[T], "Monad[U]"]) -> "Monad[U]":
        """Chain a function that maps a value to a monad."""
        ...

    def apply(self, f: "Monad[Callable[[T], U]]") -> "Monad[U]":
        """Apply a monadic function to a monad.

        This method can be overridden to provide a more efficient
        or alternative implementation.
        """
        return f.bind(lambda ff: self.bind(lambda x: self.unit(ff(x))))

    def map(self, f: Callable[[T], U]) -> "Monad[U]":
        """Map a function over a monad.

        This method can be overridden to provide a more efficient
        or alternative implementation.
        """
        return self.apply(self.unit(f))
