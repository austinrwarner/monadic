from .types.monad import Monad
from .types.iterable import Iterable
from .types.maybe import Maybe

from .option import Option, Some, Nothing
from .result import Result, Ok, Error
from .list import List
from .set import Set
from .dict import Dict

from . import _version


__version__ = _version.__version__


__all__ = [
    "Monad",
    "Iterable",
    "Maybe",
    "Option", "Some", "Nothing",
    "Result", "Ok", "Error",
    "List",
    "Set",
    "Dict"
]
