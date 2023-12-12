[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Lifecycle:Experimental](https://img.shields.io/badge/Lifecycle-Experimental-339999)](https://img.shields.io)
[![Docs:Latest](https://img.shields.io/badge/Docs-Latest-brightgreen)](https://austinrwarner.github.io/monadic/)
[![Coverage](tests/coverage.svg)]()

# monadic
Functional programming in Python using Monadic types.


## Installation

`Monadic` is available on PyPI. To install, run:

```bash
pip install monadic
```

Alternatively, to install the latest development version, run:

```bash
pip install git+https://github.com/austinrwarner/monadic.git@develop
```

## Introduction

`Monadic` is a Python library that provides a set of Monadic types and 
functions for functional programming in Python. The library is inspired 
by the functional programming primitives available in 
[Rust](https://www.rust-lang.org/), as well as pure functional programming 
languages such as [Haskell](https://www.haskell.org/),
[F#](https://fsharp.org/), and [Elm](https://elm-lang.org/).

The library exposes a generic `Monad` type that can be used to create
custom Monadic types. The library also provides a set of Monadic types
that are commonly used in functional programming, including:
- `Maybe` types that represent values that may or may not exist.
  - `Option`: Represents a value that may or may not exist.
    - `Some`: Represents a value that exists.
    - `Nothing`: Represents a value that does not exist.
  - `Result`: Represents the result of a computation that may fail.
    - `Ok`: Represents a successful computation.
    - `Error`: Represents a failed computation.
- `Iterable` types that represent collections of values.
  - `List`: Represents a list of values.
  - `Set`: Represents a set of values.
  - `Dict`: Represents a dictionary of key-value pairs.


### What is a Monad?
Though "Monad" has a somewhat technical definition based in category theory,
in practice you can think of a Monad as a type that represents a computation
that can be chained together with other computations. 

For example, a common practice in Python is to represent an optional value as
`None`. However, this can lead to code that is difficult to read and maintain
due to the need to check for `None` values. For example, consider the following
code:

```python
from typing import Optional
from dataclasses import dataclass

@dataclass
class User:
    name: str

def get_user_name(user: Optional[User]) -> Optional[str]:
    if user is None:
        return None
    else:
        return user.name

get_user_name(None) # None
get_user_name(User("John Doe")) # "John Doe"
```

This code is difficult to read and maintain because it requires the reader to
check for `None` values. This can be improved by using the `Option` type from
`Monadic`:

```python
from monadic import Option, Nothing, Some
from dataclasses import dataclass

@dataclass
class User:
    name: str


def get_user_name(user: Option[User]) -> Option[str]:
    return user.map(lambda u: u.name)

get_user_name(Nothing()) # Nothing()
get_user_name(Some(User("John Doe"))) # Some("John Doe")
```

This code is easier to read and maintain because expresses the "happy path" of
the computation, and the `Option` type handles the "unhappy path" of the
computation. This is possible because the `Option` type is a Monad, and
therefore supports the `map` method. The `map` method allows you to chain
computations together in the context of the specific monad. In the case of the
`Option` type, the `map` method will only execute the computation if the value
exists. If the value does not exist, the `map` method will return `Nothing()`.

In addition to the `map` method, the `Option` type also supports the `bind`
method. The `bind` method is similar to the `map` method, but it allows you to
chain computations together that return a monadic type. For example, consider
the following code:

```python
from monadic import Option, Nothing, Some
from dataclasses import dataclass

@dataclass
class User:
    name: str
    email: Option[str] = Nothing()

def get_user_email(user: User) -> Option[str]:
    return user.email

Some(User("John Doe")).bind(get_user_email) # Nothing()
Some(User("John Doe", Some("john.doe@xyz.com"))).bind(get_user_email) # Some("john.doe@xyz.com")
Nothing().bind(get_user_email) # Nothing()
```

In this example, we write a function that takes a `User`, and returns the
`email` field of the `User`. The first two examples work as expcted, they
are just returning the `email` field of the `User` wrapped in a `Some`. 
However, in the third example, we call that function on a `Nothing`. In this
case, the `bind` method will return `Nothing`. There are two reasons why we 
might not be able to get the `email` field of a `User`. The first is that the
`User` does not exist, and the second is that the `User` does not have an
`email` field. The `bind` method allows us to handle both of these cases
without having to check for `None` values.


While every monad supports the `map` and `bind` methods, some monads support 
additional methods. For example, the `Option` type also provides the `default`
and `unwrap` methods. The `default` method allows you to specify a default
value to use if the value does not exist. The `unwrap` method allows you to
unwrap the value from the monad, but will raise an exception if the value does
not exist. For example:

```python
from monadic import Nothing, Some

Some("Hello World").default("Goodbye World") # Some("Hello World")
Nothing().default("Goodbye World") # Some("Goodbye World")

Some("Hello World").unwrap() # "Hello World"
Nothing().unwrap() # Raises an exception
```

`default` and `unwrap` are often used in immediate succession. For example:

```python
from monadic import Nothing, Some

Some("Hello World").default("Goodbye World").unwrap() # "Hello World"
Nothing().default("Goodbye World").unwrap() # "Goodbye World"
```

### Other Monadic Types

#### Result

The `Result` type is similar to the `Option` type, but it is used to represent
the result of a computation that may fail. The `Result` type has two possible
values: `Ok` and `Error`. The `Ok` value represents a successful computation,
and the `Error` value represents a failed computation. For example:

```python
from monadic import Result, Ok, Error

Ok("Hello World") # Ok("Hello World")
Error(TypeError()) # Error(TypeError())
```

The `Result` type supports all the same methods as the `Option` type, but the 
semantics are slightly different. If any of the chained computations raise an
exception, the `Result` type will return an `Error` value. For example:

```python
from monadic import Ok

Ok(1).map(lambda x: x / 2) # Ok(0.5)
Ok(1).map(lambda x: x / 0) # Error(ZeroDivisionError())
```

The `Result` type also has a static method, `attempt`, that allows you to
execute a computation that may raise an exception. For example:

```python
from monadic import Result

Result.attempt(lambda x, y: x / y, ZeroDivisionError, 1, 2) # Ok(0.5)
Result.attempt(lambda x, y: x / y, ZeroDivisionError, 1, 0) # Error(ZeroDivisionError())
Result.attempt(lambda x, y: x / y, TypeError, 1, 0) # Raises ZeroDivisionError
```

This is the monadic equivalent of the `try`/`except` statement in Python. It even
allows you to specify the type(s) of exception to catch, and will raise an exception
if the wrong type of exception is raised.


#### List

The `List` type is used to represent a list of values. The `map` method on the
`List` type will apply the given function to each value in the list. For example:

```python
from monadic import List

List([1, 2, 3]).map(lambda x: x * 2) # List([2, 4, 6])
```

`List` is immutable, so rather than mutating the list in place, the `append` 
and `concat` methods will return a new list with the given value appended to
the end of the list. For example:

```python
from monadic import List

List([1, 2, 3]).append(4) # List([1, 2, 3, 4])
List([1, 2, 3]).concat([4, 5, 6]) # List([1, 2, 3, 4, 5, 6])
```

The `List` type also supports the `filter` method, which will filter the list
based on the given predicate. For example:

```python
from monadic import List

List([1, 2, 3]).filter(lambda x: x % 2 == 0) # List([2])
```

The `List` type also supports the `fold` method, which will fold the list into
a single value using the given function. For example:

```python
from monadic import List

List([1, 2, 3]).fold(lambda acc, x: acc + x, 0) # 6
```

The `List` type is a type of `Iterable`. Other `Iterable` types provided by
`Monadic` include `Set` and `Dict`, which have similar methods and semantics.