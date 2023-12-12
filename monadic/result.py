from typing import Callable, TypeVar, Tuple, Type, Union
from abc import ABC, abstractmethod

from .interfaces.maybe import Maybe, UnwrapError


T = TypeVar("T")
U = TypeVar("U")


class UnspecifiedException(Exception):
    def __repr__(self):
        return ''


class Result(Maybe[T], ABC):
    """Monadic type representing the result of a computation that may fail.

    This class is a subclass of :class:`Maybe` that implements the
    :class:`Monad` interface. It is a wrapper type that represents the
    result of a computation that may fail. It has two subclasses:
    - :class:`Ok`
    - :class:`Error`
    """
    @classmethod
    def unit(cls, value: T) -> "Ok[T]":  # type: ignore[override]
        """Wrap a value in an :class:`Ok` instance."""
        return Ok(value)

    @abstractmethod
    def bind(  # type: ignore[override]
            self,
            f: Callable[[T], "Result[U]"]
    ) -> "Result[U]":
        """Chain a function that maps a value to a :class:`Result`.

        If :code:`self` is an :class:`Ok`, apply the function to the
        wrapped value. Otherwise (:code:`self` is an :class:`Error`),
        return :code:`self`.

        Parameters
        ----------
        f : Callable[[T], Result[U]]
            The function to apply to the wrapped value
        """
        ...  # pragma: nocover

    def apply(  # type: ignore[override]
            self,
            f: "Result[Callable[[T], U]]"
    ) -> "Result[U]":
        """Apply a function wrapped in an :class:`Result`.

        If :code:`self` and :code:`f` are both :class:`Ok` instances,
        apply the function to the wrapped value and wrap in an :class:`Ok`.
        Otherwise, return :code:`self`.

        If an exception is raised while applying the function, return
        an :class:`Error` wrapping the exception.

        Parameters
        ----------
        f : Result[Callable[[T], U]]
            The function to apply to the wrapped value
        """
        if isinstance(f, Ok):
            return self.map(f.value)
        elif isinstance(f, Error):
            return f
        else:  # pragma: nocover
            return Error(
                TypeError(f"Cannot apply {f} to {self}")
            )

    def map(  # type: ignore[override]
            self,
            f: Callable[[T], U]
    ) -> "Result[U]":
        """Map a function over the wrapped value.

        If :code:`self` is an :class:`Ok`, apply the function to the
        wrapped value and wrap in an :class:`Ok`. Otherwise
        (:code:`self` is an :class:`Error`), return :code:`self`.

        If an exception is raised while applying the function, return
        an :class:`Error` wrapping the exception.

        Parameters
        ----------
        f : Callable[[T], U]
            The function to apply to the wrapped value
        """
        def _wrap_exception(t: T) -> Result[U]:
            try:
                return Ok(f(t))
            except Exception as e:
                return Error(e)

        return self.bind(_wrap_exception)  # type: ignore[return-value]

    @staticmethod
    def attempt(
            __f: Callable[..., T],
            __catch: Union[Type[Exception], Tuple[Type[Exception], ...]],
            *args,
            **kwargs
    ) -> "Result[T]":
        """Attempt to call a function that may raise an exception.

        If the function raises an exception, return an :class:`Error`

        Parameters
        ----------
        __f : Callable[..., T]
            The function to call
        __catch : Union[Type[Exception], Tuple[Type[Exception], ...]]
            The types of exceptions to catch
        *args
            Positional arguments to pass to the function
        **kwargs
            Keyword arguments to pass to the function
        """
        try:
            return Ok(__f(*args, **kwargs))
        except __catch as e:
            return Error(e)


class Ok(Result[T]):
    """Result type representing a successful computation.

    This class is a subclass of :class:`Result` that represents a
    successful computation. It has a :code:`value` attribute that
    contains the wrapped value. :code:`Ok` instances are truthy.
    """
    value: T

    def __init__(self, value: T):
        self.value = value

    def bind(  # type: ignore[override]
            self,
            f: Callable[[T], "Result[U]"]
    ) -> "Result[U]":
        return f(self.value)

    def unwrap(self) -> T:
        return self.value

    def __repr__(self):
        return f"Ok({repr(self.value)})"

    def __bool__(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Ok) and self.value == other.value


class Error(Result):
    """Result type representing a failed computation.

    This class is a subclass of :class:`Result` that represents a
    failed computation. It has an :code:`exception` attribute that
    contains the exception that was raised. :code:`Error` instances
    are falsy.
    """
    exception: Exception

    def __init__(self, exception: Exception = UnspecifiedException()):
        self.exception = exception

    def bind(  # type: ignore[override]
            self,
            f: Callable[[T], "Result[U]"]
    ) -> "Result[U]":
        return self

    def unwrap(self):
        raise UnwrapError('Cannot unwrap "Error"') from self.exception

    def __repr__(self):
        return f"Error({repr(self.exception)})"

    def __bool__(self):
        return False
