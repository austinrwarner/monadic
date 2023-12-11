from monadic import Dict, List, Set
from monadic.option import Some, Nothing


def test_unit():
    assert Dict.unit((1, 2)) == Dict({1: 2})


def test_empty():
    assert Dict.empty() == Dict({})


def test_from_iterable():
    assert Dict.from_iterable(((1, 2), (3, 4))) == Dict({1: 2, 3: 4})


def test_bind():
    assert Dict({1: 2, 3: 4}).bind(lambda x: Dict({x[1]: x[0]})) == Dict({2: 1, 4: 3})


def test_apply():
    assert Dict({1: 2, 3: 4, 5: 6}).apply(
        Dict({
            1: lambda x: (x[0], str(x[1])),
            3: lambda x: (x[0], float(x[1]))
        })
    ) == Dict({1: '2', 3: 4.0, 5: 6})


def test_apply_keys():
    assert Dict({1: 2, 3: 4, 5: 6}).apply_keys(
        Dict({
            1: str,
            3: float
        })
    ) == Dict({'1': 2, 3.0: 4, 5: 6})


def test_apply_values():
    assert Dict({1: 2, 3: 4, 5: 6}).apply_values(
        Dict({
            1: str,
            3: float
        })
    ) == Dict({1: '2', 3: 4.0, 5: 6})


def test_map():
    assert Dict({1: 2, 3: 4}).map(lambda x: (str(x[0]), float(x[1]))) == Dict({'1': 2.0, '3': 4.0})


def test_map_keys():
    assert Dict({1: 2, 3: 4}).map_keys(str) == Dict({'1': 2, '3': 4})


def test_map_values():
    assert Dict({1: 2, 3: 4}).map_values(float) == Dict({1: 2.0, 3: 4.0})


def test_repr():
    assert repr(Dict({1: 2})) == "Dict({1: 2})"


def test_concat():
    assert Dict({1: 2, 3: 4}).concat(Dict({5: 6, 7: 8})) == Dict({1: 2, 3: 4, 5: 6, 7: 8})


def test_iter():
    assert set(Dict({1: 2, 3: 4})) == {(1, 2), (3, 4)}


def test_keys():
    assert Dict({1: 2, 3: 4}).keys() == Set({1, 3})


def test_values():
    assert Dict({1: 2, 3: 4}).values() == List([2, 4])


def test_eq():
    assert Dict({1: 2, 3: 4}) == Dict({1: 2, 3: 4})


def test_neq():
    assert Dict({1: 2, 3: 4}) != Dict({5: 6, 7: 8})
    assert Dict({1: 2, 3: 4}) != {1: 2, 3: 4}
    assert Dict({1: 2, 3: 4}) != 1
    assert Dict({1: 2, 3: 4}) != "Dict({1: 2, 3: 4})"


def test_filter():
    assert Dict({1: 2, -1: -2}).filter(lambda x: x[0] > 0) == Dict({1: 2})


def test_filter_keys():
    assert Dict({1: 2, -1: 2}).filter_keys(lambda x: x > 0) == Dict({1: 2})


def test_filter_values():
    assert Dict({1: 2, 2: -2}).filter_values(lambda x: x > 0) == Dict({1: 2})


def test_fold():
    assert Dict({1: 2, 3: 4}).fold(lambda x, y: (x[0] + y[0], x[1] + y[1])) == (4, 6)
    assert Dict({1: 2, 3: 4}).fold(lambda x, y: (x[0] + y[0], x[1] + y[1]), (10, 10)) == (14, 16)


def test_get():
    assert Dict({1: 2, 3: 4}).get(1) == Some(2)
    assert Dict({1: 2, 3: 4}).get(2) == Nothing()


def test_set():
    assert Dict({1: 2, 3: 4}).set(5, 6) == Dict({1: 2, 3: 4, 5: 6})
    assert Dict({1: 2, 3: 4}).set(3, 6) == Dict({1: 2, 3: 6})
