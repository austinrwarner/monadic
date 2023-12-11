import pytest

from monadic.types.maybe import UnwrapError
from monadic.result import Result, Ok, Error


def map_result(result: Result[str]) -> Result[int]:
    return result.map(float).map(lambda x: x + 1).map(int)


def test_result_unit():
    assert Result.unit(1) == Ok(1)


def test_map():
    assert map_result(Ok('1')) == Ok(2.0)
    error = map_result(Ok('a'))
    assert isinstance(error, Error) and isinstance(error.exception, ValueError)


def test_apply():
    assert Ok(1).apply(Ok(str)) == Ok('1')
    assert isinstance(Ok(1).apply(Error()), Error)
    assert isinstance(Error().apply(Ok(str)), Error)
    assert isinstance(Error().apply(Error()), Error)


def test_bind():
    def ensure_positive(x: float) -> Result[float]:
        return Ok(x) if x > 0 else Error(ValueError())

    assert Ok(1).bind(ensure_positive) == Ok(1)
    assert isinstance(Ok(-1).bind(ensure_positive), Error)
    assert isinstance(Error().bind(ensure_positive), Error)


def test_unwrap():
    assert Ok(1).unwrap() == 1
    with pytest.raises(UnwrapError):
        Error().unwrap()


def test_default():
    assert Ok(1).default(2).unwrap() == 1
    assert Error().default(2).unwrap() == 2


def test_repr():
    assert repr(Ok(1)) == "Ok(1)"
    assert repr(Error()) == "Error()"
    assert repr(Error(ValueError())) == "Error(ValueError())"
