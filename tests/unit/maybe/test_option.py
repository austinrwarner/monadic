import pytest

from monadic.interfaces.maybe import UnwrapError
from monadic.option import Option, Some, Nothing


def map_option(option: Option[int]) -> Option[str]:
    return option.map(float).map(lambda x: x + 1).map(str)


def test_option_unit():
    assert Option.unit(1) == Some(1)


def test_map():
    assert map_option(Some(1)) == Some('2.0')
    assert map_option(Nothing()) == Nothing()


def test_apply():
    assert Some(1).apply(Some(str)) == Some('1')
    assert Some(1).apply(Nothing()) == Nothing()
    assert Nothing().apply(Some(str)) == Nothing()
    assert Nothing().apply(Nothing()) == Nothing()


def test_bind():
    def ensure_positive(x: float) -> Option[float]:
        return Some(x) if x > 0 else Nothing()

    assert Some(1).bind(ensure_positive) == Some(1)
    assert Some(-1).bind(ensure_positive) == Nothing()
    assert Nothing().bind(ensure_positive) == Nothing()


def test_unwrap():
    assert Some(1).unwrap() == 1
    with pytest.raises(UnwrapError):
        Nothing().unwrap()


def test_default():
    assert Some(1).default(2).unwrap() == 1
    assert Nothing().default(2).unwrap() == 2


def test_repr():
    assert repr(Some(1)) == "Some(1)"
    assert repr(Nothing()) == "Nothing()"
