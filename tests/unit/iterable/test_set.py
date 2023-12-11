from monadic import List, Set


def test_unit():
    assert Set.unit(1) == Set({1})


def test_empty():
    assert Set.empty() == Set(set())


def test_from_iterable():
    assert Set.from_iterable((1, 2, 3)) == Set({1, 2, 3})


def test_bind():
    assert Set({1, 2, 3}).bind(lambda x: Set({x, str(x)})) == Set({1, '1', 2, '2', 3, '3'})


def test_apply():
    assert Set({1, 2, 3}).apply(Set({str, float})) == Set({'1', 2.0})


def test_map():
    assert Set({1, 2, 3}).map(lambda x: x + 1) == Set({2, 3, 4})


def test_repr():
    assert repr(Set({1, 2, 3})) == "Set({1, 2, 3})"


def test_concat():
    assert Set({1, 2, 3}).concat(Set({4, 5, 6})) == Set({1, 2, 3, 4, 5, 6})
    assert Set({1, 2, 3}).concat(List({4, 5, 6})) == Set({1, 2, 3, 4, 5, 6})


def test_iter():
    assert set(Set({1, 2, 3})) == {1, 2, 3}


def test_eq():
    assert Set({1, 2, 3}) == Set({1, 2, 3})


def test_neq():
    assert Set({1, 2, 3}) != Set({4, 5, 6})
    assert Set({1, 2, 3}) != {1, 2, 3}
    assert Set({1, 2, 3}) != 1
    assert Set({1, 2, 3}) != "Set({1, 2, 3})"


def test_filter():
    assert Set({1, 2, 3}).filter(lambda x: x % 2 == 0) == Set({2})


def test_fold():
    assert Set({1, 2, 3}).fold(lambda x, y: x + y) == 6
    assert Set({1, 2, 3}).fold(lambda x, y: x + y, 10) == 16
