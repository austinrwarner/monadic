from monadic import List, Set


def test_unit():
    assert List.unit(1) == List([1])


def test_empty():
    assert List.empty() == List([])


def test_from_iterable():
    assert List.from_iterable((1, 2, 3)) == List([1, 2, 3])


def test_bind():
    assert List([1, 2, 3]).bind(lambda x: List([x, str(x)])) == List([1, '1', 2, '2', 3, '3'])


def test_apply():
    assert List([1, 2, 3]).apply(List([str, float])) == List(['1', 2.0])


def test_map():
    assert List([1, 2, 3]).map(lambda x: x + 1) == List([2, 3, 4])


def test_repr():
    assert repr(List([1, 2, 3])) == "List([1, 2, 3])"


def test_concat():
    assert List([1, 2, 3]).concat(List([4, 5, 6])) == List([1, 2, 3, 4, 5, 6])
    assert List([1, 2, 3]).concat(Set([4, 5, 6])) == List([1, 2, 3, 4, 5, 6])


def test_iter():
    assert list(List([1, 2, 3])) == [1, 2, 3]


def test_eq():
    assert List([1, 2, 3]) == List([1, 2, 3])


def test_neq():
    assert List([1, 2, 3]) != List([4, 5, 6])
    assert List([1, 2, 3]) != [1, 2, 3]
    assert List([1, 2, 3]) != 1
    assert List([1, 2, 3]) != "List([1, 2, 3])"


def test_filter():
    assert List([1, 2, 3]).filter(lambda x: x % 2 == 0) == List([2])


def test_fold():
    assert List([1, 2, 3]).fold(lambda x, y: x + y) == 6
    assert List([1, 2, 3]).fold(lambda x, y: x + y, 10) == 16
