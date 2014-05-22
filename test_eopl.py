import itertools
import numbers
import random
import nose.tools as nt
from eopl import *


def test_is_number():
    nt.assert_true(is_number(1.))
    nt.assert_true(is_number(1))
    nt.assert_true(is_number(1j))
    nt.assert_false(is_number([]))
    nt.assert_false(is_number(''))
    nt.assert_false(is_number(object()))


def test_is_list():
    nt.assert_true(is_list([]))
    nt.assert_true(is_list([1, 2, 3]))
    nt.assert_true(is_list([1, 2, '3']))
    nt.assert_false(is_list(1))
    nt.assert_false(is_list('a'))


def test_car():
    x = [1, 2, 3]
    r = car(x)
    nt.assert_equal(r, 1)


def test_cdr():
    x = [1, 2, 3]
    r = cdr(x)
    nt.assert_equal(r, [2, 3])


def test_head():
    x = [1, 2, 3, 'a', object(), [1, 2]]
    r = head(x, 2)
    nt.assert_equal(r, [1, 2])


def test_tail():
    x = [1, 2, 3, 'a', object(), [1, 2]]
    r = tail(x, 3)
    nt.assert_equal(r, x[-3:])


def test_every():
    x = []
    # empty is true for all predicates
    r = every(lambda x: False, x)
    nt.assert_true(r)

    x = [1, 2, -1, 3]
    r = every(lambda x: x > 1, x)
    nt.assert_false(r)


def test_exists():
    x = []
    # empty is false for all predicates
    r = exists(lambda x: 0, x)
    nt.assert_false(r)

    x = [1, 2, -1, 3]
    r = exists(lambda x: x > 1, x)
    nt.assert_true(r)


def test_duple():
    x = random.random()
    n = 2
    r = duple(n, x)
    nt.assert_equal(r, [x] * n)


def test_reverse():
    x = [1, 2, 3]
    r = reverse(x)
    nt.assert_equal(r, x[::-1])


def test_invert():
    x = [['a', 1], ['a', 2]]
    r = invert(x)
    expected = [[1, 'a'], [2, 'a']]
    nt.assert_equal(r, expected)


def test_concat():
    x = [1, 2, 'a', object()]
    y = ['c', 3, 4, 5, 'b']
    r = concat(x, y)
    e = x + y
    nt.assert_equal(r, e)


def test_cadr():
    x = [1, 2, 3]
    r = cadr(x)
    e = x[1]
    nt.assert_equal(r, e)


def test_filter_in():
    x = [1, 2, list('abc'), 'd', 34, 3.0]
    r = filter_in(lambda x: isinstance(x, (list, str)), x)
    e = [list('abc'), 'd']
    nt.assert_equal(r, e)

    x = [1, 2, list('abc'), 'd', 34, 3.0]
    r = filter_in(lambda x: isinstance(x, numbers.Number), x)
    e = [1, 2, 34, 3.0]
    nt.assert_equal(r, e)


def test_length():
    x = ['a', 'b', 3, 4]
    r = length(x)
    e = len(x)
    nt.assert_equal(r, e)


def test_list_ref():
    x = list(range(10))
    r = list_ref(x, 3)
    e = x[3]
    nt.assert_equal(r, e)


def test_list_set():
    x = ['a', 1, ['d', 'e', object()]]
    r = list_set(x, 2, [1, 2])
    e = x[:2] + [[1, 2]]
    nt.assert_equal(r, e)


def test_product():
    xys = [[[], []],
           [[1, 2], []],
           [[1], [2]],
           [[1], [2, 3]],
           [[1, 2], [3, 4]]]
    for x, y in xys:
        r = product(x, y)
        e = list(map(list, list(itertools.product(x, y))))
        nt.assert_equal(r, e)


def test_list_append():
    x = [1, 2, 3]
    y = ['a', 'b', object(), 3.4]
    r = list_append(x, y)
    e = x + y
    nt.assert_equal(r, e)


def test_down():
    x = ['a', 2.24, 1, object()]
    r = down(x)
    e = list(map(lambda x: [x], x))
    nt.assert_equal(r, e)

    x = [['a', 2.24], 1, object()]
    r = down(x)
    e = list(map(lambda x: [x], x))
    nt.assert_equal(r, e)
