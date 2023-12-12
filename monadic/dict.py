from typing import TypeVar, Union, Tuple, Callable, Hashable
import typing

from .interfaces import Iterable
from .set import Set
from .list import List
from .option import Some, Nothing, Option

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")

K2 = TypeVar("K2", bound=Hashable)
V2 = TypeVar("V2")


class Dict(Iterable[Tuple[K, V]]):
    """A monadic dictionary.

    This is a wrapper around the built-in dict type that implements the
    :class:`Iterable` interface. Following a functional style, it is
    immutable. To add an item to the dictionary by key, use :meth:`set`.

    This class is considered an iterable of tuples, where the first item
    in the tuple is the key and the second item is the value. This differs
    from the built-in dict type, which is an iterable of keys. To get the
    keys of a :class:`Dict`, use the :meth:`keys` method. To get the values
    of a :class:`Dict`, use the :meth:`values` method.

    Parameters
    ----------
    inner : typing.Iterable[Tuple[K, V]]
        The iterable of tuples containing the key-value pairs to wrap as a
        dictionary. Alternatively, a dictionary can be passed in directly.

    Examples
    --------
    >>> from monadic.dict import Dict
    >>> Dict({"a": 1, "b": 2, "c": 3}).get("a")
    Some(1)
    >>> Dict({"a": 1, "b": 2, "c": 3}).get("d")
    Nothing()
    >>> Dict({"a": 1, "b": 2, "c": 3}).set("d", 4)
    Dict({'a': 1, 'b': 2, 'c': 3, 'd': 4})
    """
    inner: typing.Dict[K, V]

    def __init__(
            self,
            inner: Union[
                typing.Iterable[Tuple[K, V]],
                typing.Dict[K, V]
            ]
    ):
        self.inner = dict(inner)

    @classmethod
    def from_iterable(  # type: ignore[override]
            cls,
            iterable: typing.Iterable[Tuple[K2, V2]]
    ) -> "Dict[K2, V2]":
        return Dict(iterable)

    @classmethod
    def unit(  # type: ignore[override]
            cls,
            value: Tuple[K2, V2]
    ) -> "Dict[K2, V2]":
        return cls.from_iterable((value,))

    def bind(  # type: ignore[override]
        self, f: Callable[[Tuple[K, V]], "Dict[K2, V2]"]
    ) -> "Dict[K2, V2]":
        """Chain a function that maps a value to a dictionary.

        Parameters
        ----------
        f : Callable[[Tuple[K, V]], Dict[K2, V2]]
            A function that maps a value to a dictionary.

        Returns
        -------
        Dict[K2, V2]
            The result of applying the function to each key-value pair in the
            dictionary and concatenating the results.
        """
        return Dict.from_iterable(
            fx for x in self for fx in f(x)
        )

    def apply(  # type: ignore[override]
            self,
            f: "Dict[K, Callable[[Tuple[K, V]], Tuple[K2, V2]]]"
    ) -> "Dict[Union[K, K2], Union[V, V2]]":
        """Apply a dictionary of functions to a dictionary.

        For each key-value pair in the dictionary, if the key is present in
        the dictionary of functions, the function is applied to the key-value
        pair and the result is added to the result dictionary. If the key is
        not present in the dictionary of functions, the key-value pair is
        ignored.

        Parameters
        ----------
        f : Dict[K, Callable[[Tuple[K, V]], Tuple[K2, V2]]]
            A dictionary of functions.

        Returns
        -------
        Dict[Union[K, K2], Union[V, V2]]
            The result of applying the corresponding function to each
            key-value pair in the dictionary and concatenating the
            results.
        """
        return self.from_iterable(
            f.get(k).unwrap()((k, v))
            for k, v in self
            if f.get(k)
        )

    def apply_keys(
            self,
            f: "Dict[K, Callable[[K], K2]]"
    ) -> "Dict[Union[K, K2], V]":
        """Apply a dictionary of functions to the keys of a dictionary.

        This method is similar to :meth:`apply`, but only applies the
        functions to the keys of the dictionary, leaving the values
        unchanged.
        """
        def accept_tuple(v):
            return lambda x: (v(x[0]), x[1])

        return self.apply(
            Dict.from_iterable(
                (k, accept_tuple(v))
                for k, v in f
            )
        )

    def apply_values(
            self,
            f: "Dict[K, Callable[[V], V2]]"
    ) -> "Dict[K, Union[V, V2]]":
        """Apply a dictionary of functions to the values of a dictionary.

        This method is similar to :meth:`apply`, but only applies the
        functions to the values of the dictionary, leaving the keys
        unchanged.
        """
        def accept_tuple(v):
            return lambda x: (x[0], v(x[1]))

        return self.apply(
            Dict.from_iterable(
                (k, accept_tuple(v))
                for k, v in f
            )
        )

    def map(  # type: ignore[override]
            self,
            f: Callable[[Tuple[K, V]], Tuple[K2, V2]]
    ) -> "Dict[K2, V2]":
        """Map a function over a dictionary.

        Parameters
        ----------
        f : Callable[[Tuple[K, V]], Tuple[K2, V2]]
            A function that maps a key-value pair to a new key-value pair.

        Returns
        -------
        Dict[K2, V2]
            A new dictionary containing the results of applying the function
            to each key-value pair in the original dictionary.
        """
        return self.from_iterable((f((k, v)) for k, v in self))

    def map_keys(
            self,
            f: Callable[[K], K2]
    ) -> "Dict[K2, V]":
        """Map a function over the keys of a dictionary.

        This method is similar to :meth:`map`, but only applies the
        function to the keys of the dictionary, leaving the values
        unchanged.
        """
        return self.map(lambda x: (f(x[0]), x[1]))

    def map_values(
            self,
            f: Callable[[V], V2]
    ) -> "Dict[K, V2]":
        """Map a function over the values of a dictionary.

        This method is similar to :meth:`map`, but only applies the
        function to the values of the dictionary, leaving the keys
        unchanged.
        """
        return self.map(lambda x: (x[0], f(x[1])))

    @classmethod
    def empty(cls) -> "Dict":
        """Create an empty dictionary."""
        return cls.from_iterable([])

    def __repr__(self):
        return f"Dict({self.inner})"

    def concat(  # type: ignore[override]
            self,
            other: "Iterable[Tuple[K2, V2]]"
    ) -> "Dict[Union[K, K2], Union[V, V2]]":
        return super().concat(other)  # type: ignore[return-value]

    def filter(  # type: ignore[override]
            self,
            f: Callable[[Tuple[K, V]], bool]
    ) -> "Dict[K, V]":
        """Filter a dictionary by a predicate.

        The predicate is a function that takes a key-value pair and returns
        a boolean. If the predicate returns True, the key-value pair is
        included in the result. If the predicate returns False, the key-value
        pair is excluded from the result.

        Parameters
        ----------
        f : Callable[[Tuple[K, V]], bool]
            A predicate function.

        Returns
        -------
        Dict[K, V]
            A new dictionary containing only the key-value pairs for which
            the predicate returns True.
        """
        return self.from_iterable(filter(f, self))

    def filter_keys(
            self,
            f: Callable[[K], bool]
    ) -> "Dict[K, V]":
        """Filter a dictionary by a predicate on the keys.

        This method is similar to :meth:`filter`, but only applies the
        predicate to the keys of the dictionary, ignoring the values.
        """
        return self.filter(lambda x: f(x[0]))

    def filter_values(
            self,
            f: Callable[[V], bool]
    ) -> "Dict[K, V]":
        """Filter a dictionary by a predicate on the values.

        This method is similar to :meth:`filter`, but only applies the
        predicate to the values of the dictionary, ignoring the keys.
        """
        return self.filter(lambda x: f(x[1]))

    def __iter__(self):
        return self.inner.items().__iter__()

    def keys(self) -> Set[K]:
        """Get the keys of a dictionary.

        Returns
        -------
        Set[K]
            A set containing the keys of the dictionary.
        """
        return Set.from_iterable(self.inner.keys())

    def values(self) -> List[V]:
        """Get the values of a dictionary.

        Returns
        -------
        List[V]
            A list containing the values of the dictionary.
        """
        return List.from_iterable(self.inner.values())

    def get(self, key: K) -> Option[V]:
        """Get a value from a dictionary by key.

        Parameters
        ----------
        key : K
            The key to look up in the dictionary.

        Returns
        -------
        Option[V]
            A :class:`Some` containing the value if the key is present in
            the dictionary, or :class:`Nothing` if the key is not present.
        """
        try:
            return Some(self.inner[key])
        except KeyError:
            return Nothing()

    def set(
            self,
            key: K2,
            value: V2
    ) -> "Dict[Union[K, K2], Union[V, V2]]":
        """Add a key-value pair to a dictionary.

        Parameters
        ----------
        key : K2
            The key to add.
        value : V2
            The value to add.

        Returns
        -------
        Dict[Union[K, K2], Union[V, V2]]
            A new dictionary containing the old contents and the new key-value
            pair.
        """
        return self.append((key, value))  # type: ignore[return-value]

    def drop(self, key: K) -> "Dict[K, V]":
        """Remove a key-value pair from a dictionary.

        Parameters
        ----------
        key : K
            The key to remove.

        Returns
        -------
        Dict[K, V]
            A new dictionary containing the old contents without the key-value
            pair.
        """
        return self.filter_keys(lambda x: x != key)

    def __eq__(self, other):
        return isinstance(other, Dict) and self.inner == other.inner
