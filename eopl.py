import operator
import collections
import numbers
from operator import eq
from functools import partial


def isa(typ):
    return lambda x: isinstance(x, typ)


is_number = isa(numbers.Number)
is_list = isa(list)
is_list_like = lambda x: (not isinstance(x, basestring) and
                          isinstance(x, collections.Iterable))


#### utilities


def head(lst, n):
    if not n:
        return []
    return cons(car(lst), head(cdr(lst), n - 1))


def tail(lst, n):
    return reverse(head(reverse(lst), n))


def compose2(f, g):
    return lambda *args, **kwargs: f(g(*args, **kwargs))


def compose(*funcs):
    if len(funcs) == 1:
        return list(funcs).pop()
    return reduce(compose2, funcs)


def cons(head, tail):
    return [head] + tail


def manuf(s):
    s = s.lstrip('c').rstrip('r')
    d = {'a': car, 'd': cdr}
    return reduce(compose2, map(d.__getitem__, s))


def car(lst):
    return lst[0]


def cdr(lst):
    return lst[1:]


cddr = manuf('cddr')
cadr = manuf('cadr')
caddr = manuf('caddr')


#### 1.16

def every(pred, lst):
    return not lst or (pred(car(lst)) and every(pred, cdr(lst)))


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
    # TODO: extend to *args number of lists
    if not (los1 and los2):
        # cartesian product of empty things is empty
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


def lsum(lst):
    if not lst:
        return 0
    return car(lst) + lsum(cdr(lst))


def lmap(f, lst):
    if not lst:
        return []
    return cons(f(car(lst)), lmap(f, cdr(lst)))


#### 1.17

def flatten(lst):
    """Flatten an arbitrarily nested list"""
    if not lst:
        return []
    if not is_list_like(car(lst)):
        return concat([car(lst)], flatten(cdr(lst)))
    return concat(flatten(car(lst)), flatten(cdr(lst)))


def count_occurrences(s, lst):
    return length(filter_in(partial(eq, s), flatten(lst)))


def merge(lst1, lst2):
    if not lst1 and lst2:
        return lst2
    if not lst2 and lst1:
        return lst1
    if not (lst2 or lst1):
        return []
    if car(lst1) <= car(lst2):
        return concat(cons(car(lst1), [car(lst2)]), merge(cdr(lst1),
                                                          cdr(lst2)))
    return concat(cons(car(lst2), [car(lst1)]), merge(cdr(lst1), cdr(lst2)))


def up(lst):
    if not lst:
        return []
    if not is_list_like(car(lst)):
        return cons(car(lst), up(cdr(lst)))
    return concat(car(lst), up(cdr(lst)))


def swapper(a, b, lst):
    if not lst:
        return []
    to_cons = c = car(lst)
    if c == a:
        to_cons = b
    elif c == b:
        to_cons = a
    elif is_list_like(c):
        to_cons = swapper(a, b, c)
    return cons(to_cons, swapper(a, b, cdr(lst)))


def path(x, bst):
    if not bst:
        return []
    if eq(car(bst), x):
        return []
    if car(bst) < x:
        return cons('right', path(x, caddr(bst)))
    return cons('left', path(x, cadr(bst)))


def filt(pred, lst):
    if not lst:
        return []
    if not pred(car(lst)):
        return filt(pred, cdr(lst))
    return cons(car(lst), filt(pred, cdr(lst)))


def sort(lst):
    return sortp(operator.lt, lst)


def sortp(pred, lst):
    if length(lst) <= 1:
        return lst
    piv = list_ref(lst, int(length(lst) / 2))
    lhs = filt(lambda x: pred(x, piv), lst)
    rhs = filt(lambda x: not pred(x, piv) and x != piv, lst)
    return concat(sortp(pred, lhs), cons(piv, sortp(pred, rhs)))


def car_cdr(s, lst, errvalue):
    if not lst:
        return lambda x: errvalue
    if eq(car(lst), s):
        return car
    if is_list_like(car(lst)):
        return compose(car_cdr(s, car(lst), errvalue), car)
    return compose(car_cdr(s, cdr(lst), errvalue), cdr)
