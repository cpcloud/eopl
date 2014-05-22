import itertools
import numbers
import operator


eq = operator.eq


def isa(typ):
    return lambda x: isinstance(x, typ)


is_number = isa(numbers.Number)
is_list = isa(list)


def head(lst, n):
    if not n:
        return []
    return cons(car(lst), head(cdr(lst), n - 1))


def tail(lst, n):
    return reverse(head(reverse(lst), n))


def compose2(f, g):
    return lambda *args, **kwargs: f(g(*args, **kwargs))


def compose(*funcs):
    return reduce(compose2, funcs)


def cons(head, tail):
    return [head] + tail


def car(lst):
    return lst[0]


def cdr(lst):
    return lst[1:]


def ncdr(n):
    return compose(*itertools.repeat(cdr, n))


def every(pred, lst):
    return (not lst) or (pred(car(lst)) and every(pred, cdr(lst)))


def exists(pred, lst):
    return lst and (pred(car(lst)) or exists(pred, cdr(lst)))


def duple(n, x):
    if not n:
        return []
    elif n == 1:
        return [x]
    return concat([x], duple(n - 1, x))


def reverse(lst):
    if not lst:
        return []
    return concat(reverse(cdr(lst)), [car(lst)])


def invert(lst):
    if not lst:
        return []
    return concat([reverse(car(lst))], invert(cdr(lst)))


def cadr(lst):
    return car(cdr(lst))


def concat(lst1, lst2):
    if not (lst1 or lst2):
        return []
    if not lst1:
        return lst2
    if not lst2:
        return lst1
    return cons(car(lst1), concat(cdr(lst1), lst2))


def filter_in(pred, lst):
    if not lst:
        return []
    if not pred(car(lst)):
        return filter_in(pred, cdr(lst))
    return cons(car(lst), filter_in(pred, cdr(lst)))


def length(x):
    if not x:
        return 0
    return 1 + length(x[1:])


def list_ref(x, i):
    """0-based list index"""
    assert 0 <= i < length(x)
    if i == 0:
        return car(x)
    return list_ref(cdr(x), i - 1)


def list_set(lst, n, x):
    assert 0 <= n < length(lst)
    if not n:
        return cons(x, cdr(lst))
    return cons(car(lst), list_set(cdr(lst), n - 1, x))


def product(los1, los2):
    """
    product([1], [2]) -> [[1, 2]]
    product([1], [2, 3]) -> [[1, 2], [1, 3]]
    product([1, 2], [3, 4]) -> [[1, 3], [1, 4], [2, 3], [2, 4]]
    """
    if not (los1 and los2):
        return []
    return cons([car(los1), car(los2)],
                concat(product([car(los1)], cdr(los2)),
                       product(cdr(los1), los2)))


def list_append(lst, toapp):
    if not toapp:
        return lst
    return list_append(concat(lst, toapp[:1]), toapp[1:])


def down(lst):
    if not cdr(lst):
        return [lst]
    return cons([car(lst)], down(cdr(lst)))
