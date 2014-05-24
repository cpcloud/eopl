import itertools
import numbers
import random
import operator
import nose.tools as nt
from eopl import *


def test_numberp():
    nt.assert_true(numberp(1.))
    nt.assert_true(numberp(1))
    nt.assert_true(numberp(1j))
    nt.assert_false(numberp([]))
    nt.assert_false(numberp(''))
    nt.assert_false(numberp(object()))


def test_listp():
    nt.assert_true(listp([]))
    nt.assert_true(listp([1, 2, 3]))
    nt.assert_true(listp([1, 2, '3']))
    nt.assert_false(listp(1))
    nt.assert_false(listp('a'))


def test_list_likep():
    nt.assert_true(list_likep([]))
    nt.assert_true(list_likep([1, 2, 3]))
    nt.assert_true(list_likep([1, 2, '3']))
    nt.assert_true(list_likep(()))
    nt.assert_true(list_likep({}))
    nt.assert_false(list_likep(1))
    nt.assert_false(list_likep('a'))
    nt.assert_false(list_likep(object()))
    nt.assert_false(list_likep(test_list_likep))


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


def test_count_occurrences():
    x = ['a', [1, 2], 'd', [['d'], 'd', [[[['d']]]]]]
    s = 'd'
    r = count_occurrences(s, x)
    e = 4
    nt.assert_equal(r, e)


def test_merge():
    x, y = [1, 3, 5], [2, 4, 6]
    r = merge(x, y)
    e = list(range(1, 7))
    nt.assert_equal(r, e)

    x, y = [1, 3, 5], [3, 4, 6, 8]
    r = merge(x, y)
    e = [1, 3, 3, 4, 5, 6, 8]
    nt.assert_equal(r, e)

    x, y = [1, 3, 5, 9, 11], [3, 4, 6, 8]
    r = merge(x, y)
    e = [1, 3, 3, 4, 5, 6, 8, 9, 11]
    nt.assert_equal(r, e)


def test_up():
    x = [[1, 2], [3, 4]]
    nt.assert_equal(up(x), list(range(1, 5)))

    x = ['a', [1, 2], 'd', [['d'], 'd', [[[['d']]]]]]
    nt.assert_equal(up(down(x)), x)

    x = [['x', ['y']], 'z']
    nt.assert_equal(up(x), ['x', ['y'], 'z'])


def test_swapper():
    x = list('abcd')
    r = swapper('a', 'd', x)
    e = list('dbca')
    nt.assert_equal(r, e)

    x = [['x'], 'y', ['z', ['x']]]
    r = swapper('x', 'y', x)
    e = [['y'], 'x', ['z', ['y']]]
    nt.assert_equal(r, e)


def test_path():
    x = [14, [7, [], [12, [], []]],
         [26, [20, [17, [], []], []], [31, [], []]]]
    r = path(17, x)
    e = ['right', 'left', 'left']
    nt.assert_equal(r, e)


def test_sort():
    k = 5
    x = random.sample(list(range(10)), k)
    nt.assert_equal(sort(x), sorted(x))


def test_sortp():
    k = 5
    x = random.sample(list(range(10)), k)
    nt.assert_equal(sortp(operator.gt, x), sorted(x, reverse=True))


def test_car_cdr():
    lst = list('abc')
    s = 'a'
    r = car_cdr(s, lst, 'fail')
    e = car
    nt.assert_equal(r, e)

    lst = ['cat', 'lion', ['fish', 'dog', []], 'pig']
    s = 'dog'
    r = car_cdr(s, lst, 'fail')
    e = compose(car, compose(cdr, compose(car, compose(cdr, cdr))))
    rs = r(lst)
    nt.assert_equal(rs, e(lst))

    lst = ['b', 'c']
    r = car_cdr('a', lst, 'fail')
    nt.assert_equal(r(lst), 'fail')
