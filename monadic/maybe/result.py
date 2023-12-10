from typing import Callable, TypeVar
from abc import ABC

from .core import Maybe


T = TypeVar('T')
U = TypeVar('U')


class Result(Maybe[T], ABC):
    @classmethod
    def unit(cls, value: T) -> 'Ok[T]':
        return Ok(value)

    def _bind(self, f: Callable[[T], 'Result[U]']) -> 'Result[U]':  # type: ignore[override]
        if isinstance(self, Ok):
            return f(self.value)
        elif isinstance(self, Error):
            return self
        else:
            return Error(f'{self} is not a valid Result.')


class Ok(Result[T]):
    value: T

    def __init__(self, value: T):
        self.value = value

    def __repr__(self):
        return f'Ok({repr(self.value)})'

    def __bool__(self):
        return True


class Error(Result):
    reason: str

    def __init__(self, reason: str):
        self.reason = reason

    def __repr__(self):
        return f'Error({self.reason})'

    def __bool__(self):
        return False
