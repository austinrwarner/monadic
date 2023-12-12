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