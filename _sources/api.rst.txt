Monadic API
===========

Monad
-----
.. autoclass:: monadic.Monad
   :members:


Maybe
-----
:code:`Maybe` monads are a class of monads that represent values that may
or may not be present. :code:`Monadic` exposes two :code:`Maybe` monads,
:class:`Option` and :class:`Result`. :class:`Option` represents a value
that may or may not be present, while :class:`Result` represents the
result of an operation that may or may not have succeeded. The main
difference between the two is that :class:`Option` carries no information
about why a value may not be present, while :class:`Result` can carry an
error message explaining why an operation may have failed.


.. autoclass:: monadic.Maybe
    :members:


Option
~~~~~~
.. autoclass:: monadic.Option
    :members:
    :show-inheritance:


Some
++++
.. autoclass:: monadic.Some
    :show-inheritance:

Nothing
+++++++
.. autoclass:: monadic.Nothing
    :show-inheritance:


Result
~~~~~~
.. autoclass:: monadic.Result
    :members:
    :show-inheritance:

Ok
++
.. autoclass:: monadic.Ok
    :show-inheritance:

Error
+++++
.. autoclass:: monadic.Error
    :show-inheritance:


Iterables
---------
:code:`Iterable` monads are a class of monads that represent a collection
of values that can be iterated over. :code:`Monadic` exposes three
:code:`Iterable` monads, :class:`List`, :class:`Set`, and :class:`Dict`.
These monads each map to their respective Python types, but follow a functional
style and are immutable.

.. autoclass:: monadic.Iterable
    :members:


List
~~~~
.. autoclass:: monadic.List
    :members: bind, apply, map, zip_apply
    :show-inheritance:


Set
~~~
.. autoclass:: monadic.Set
    :members: bind, apply, map
    :show-inheritance:


Dict
~~~~
.. autoclass:: monadic.Dict
    :members:
        bind,
        apply, apply_keys, apply_values,
        map, map_keys, map_values, filter, filter_keys, filter_values,
        get, set, drop
    :show-inheritance:
