"""Provides some utilities widely used by other modules"""

# This module is safe for: from utils import *

# TODO: Priority queues may not belong here -- see treatment in search.py

import operator
import random
import os.path
import bisect

from grid import *  # noqa

# ______________________________________________________________________________
# Functions on Sequences (mostly inspired by Common Lisp)


def removeall(item, seq):
    """Return a copy of seq (or string) with all occurences of item removed."""
    if isinstance(seq, str):
        return seq.replace(item, '')
    else:
        return [x for x in seq if x != item]


def unique(seq):
    """Remove duplicate elements from seq. Assumes hashable elements."""
    return list(set(seq))


def count(seq):
    """Count the number of items in sequence that are interpreted as true."""
    return sum(bool(x) for x in seq)


def product(numbers):
    """Return the product of the numbers, e.g. product([2, 3, 10]) == 60"""
    result = 1
    for x in numbers:
        result *= x
    return result


def first(iterable, default=None):
    "Return the first element of an iterable or the next element of a generator; or default."
    try:
        return iterable[0]
    except IndexError:
        return default
    except TypeError:
        return next(iterable, default)


def every(predicate, seq):
    """True if every element of seq satisfies predicate."""

    return all(predicate(x) for x in seq)


def is_in(elt, seq):
    """Similar to (elt in seq), but compares with 'is', not '=='."""
    return any(x is elt for x in seq)

# ______________________________________________________________________________
# Functions on sequences of numbers
# NOTE: these take the sequence argument first, like min and max,
# and like standard math notation: \sigma (i = 1..n) fn(i)
# A lot of programing is finding the best value that satisfies some condition;
# so there are three versions of argmin/argmax, depending on what you want to
# do with ties: return the first one, return them all, or pick at random.


def argmin(seq, fn):
    return min(seq, key=fn)


def argmin_list(seq, fn):
    """Return a list of elements of seq[i] with
       the lowest fn(seq[i]) scores."""
    smallest_score = fn(min(seq, key=fn))

    return [elem for elem in seq if fn(elem) == smallest_score]


def argmin_gen(seq, fn):
    """Return a generator of elements of seq[i] with the
       lowest fn(seq[i]) scores.
    """

    smallest_score = fn(min(seq, key=fn))

    yield from (elem for elem in seq if fn(elem) == smallest_score)


def argmin_random_tie(seq, fn):
    """Return an element with lowest fn(seq[i]) score; break ties at random.
    Thus, for all s,f: argmin_random_tie(s, f) in argmin_list(s, f)"""
    return random.choice(argmin_list(seq, fn))


def argmax(seq, fn):
    """Return an element with highest fn(seq[i]) score;
       tie goes to first one.
    """
    return max(seq, key=fn)


def argmax_list(seq, fn):
    """Return a list of elements of seq[i] with the highest fn(seq[i]) scores.
       Not good to use 'argmin_list(seq, lambda x: -fn(x))' as method
       breaks if fn is len
    """
    largest_score = fn(max(seq, key=fn))

    return [elem for elem in seq if fn(elem) == largest_score]


def argmax_gen(seq, fn):
    """Return a generator of elements of seq[i] with
       the highest fn(seq[i]) scores.
        """
    largest_score = fn(min(seq, key=fn))

    yield from (elem for elem in seq if fn(elem) == largest_score)


def argmax_random_tie(seq, fn):
    "Return an element with highest fn(seq[i]) score; break ties at random."
    return argmin_random_tie(seq, lambda x: -fn(x))

# ______________________________________________________________________________
# Statistical and mathematical functions


def histogram(values, mode=0, bin_function=None):
    """Return a list of (value, count) pairs, summarizing the input values.
    Sorted by increasing value, or if mode=1, by decreasing count.
    If bin_function is given, map it over values first."""
    if bin_function:
        values = list(map(bin_function, values))

    bins = {}
    for val in values:
        bins[val] = bins.get(val, 0) + 1

    if mode:
        return sorted(list(bins.items()), key=lambda x: (x[1], x[0]),
                      reverse=True)
    else:
        return sorted(bins.items())


def dotproduct(X, Y):
    """Return the sum of the element-wise product of vectors X and Y."""
    return sum(x * y for x, y in zip(X, Y))


def element_wise_product(X, Y):
    """Return vector as an element-wise product of vectors X and Y"""
    assert len(X) == len(Y)
    return [x * y for x, y in zip(X, Y)]


def matrix_multiplication(X_M, *Y_M):
    """Return a matrix as a matrix-multiplication of X_M and arbitary number of matrices *Y_M"""

    def _mat_mult(X_M, Y_M):
        """Return a matrix as a matrix-multiplication of two matrices X_M and Y_M
        >>> matrix_multiplication([[1, 2, 3],
                                   [2, 3, 4]],
                                   [[3, 4],
                                    [1, 2],
                                    [1, 0]])
        [[8, 8],[13, 14]]
        """
        assert len(X_M[0]) == len(Y_M)

        result = [[0 for i in range(len(Y_M[0]))] for j in range(len(X_M))]
        for i in range(len(X_M)):
            for j in range(len(Y_M[0])):
                for k in range(len(Y_M)):
                    result[i][j] += X_M[i][k] * Y_M[k][j]
        return(result)

    result = X_M
    for Y in Y_M:
        result = _mat_mult(result, Y)

    return(result)

def vector_to_diagonal(v):
    """Converts a vector to a diagonal matrix with vector elements
    as the diagonal elements of the matrix"""
    diag_matrix = [[0 for i in range(len(v))] for j in range(len(v))]
    for i in range(len(v)):
        diag_matrix[i][i] = v[i]

    return diag_matrix

def vector_add(a, b):
    """Component-wise addition of two vectors."""
    return tuple(map(operator.add, a, b))


def scalar_vector_product(X, Y):
    """Return vector as a product of a scalar and a vector"""
    return [X*y for y in Y]

def scalar_matrix_product(X, Y):
    return([scalar_vector_product(X, y) for y in Y])

def inverse_matrix(X):
    """Inverse a given square matrix of size 2x2"""
    assert len(X) == 2
    assert len(X[0]) == 2
    det = X[0][0] * X[1][1] - X[0][1] * X[1][0]
    assert det != 0
    inv_mat = scalar_matrix_product(1.0/det, [[X[1][1], -X[0][1]], [-X[1][0], X[0][0]]])

    return(inv_mat)


def probability(p):
    "Return true with probability p."
    return p > random.uniform(0.0, 1.0)


def weighted_sample_with_replacement(seq, weights, n):
    """Pick n samples from seq at random, with replacement, with the
    probability of each element in proportion to its corresponding
    weight."""
    sample = weighted_sampler(seq, weights)

    return [sample() for _ in range(n)]


def weighted_sampler(seq, weights):
    "Return a random-sample function that picks from seq weighted by weights."
    totals = []
    for w in weights:
        totals.append(w + totals[-1] if totals else w)

    return lambda: seq[bisect.bisect(totals, random.uniform(0, totals[-1]))]

def truncate(x, n = 4):
    """Truncates floats, vectors, matrices to n decimal values"""
    if isinstance(x, float):
        return(float("{0:.{1}f}".format(x, n)))
    elif isinstance(x, list) and isinstance(x[0], float):
        return([float("{0:.{1}f}".format(i, n)) for i in x])
    elif isinstance(x, list) and isinstance(x[0], list) and isinstance(x[0][0], float):
        return([[float("{0:.{1}f}".format(i, n)) for i in row] for row in x])
    else:
        return x

def num_or_str(x):
    """The argument is a string; convert to a number if
       possible, or strip it.
    """
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return str(x).strip()


def normalize(numbers):
    """Multiply each number by a constant such that the sum is 1.0"""
    total = float(sum(numbers))
    return([(n / total) for n in numbers])


def clip(x, lowest, highest):
    """Return x clipped to the range [lowest..highest]."""
    return max(lowest, min(x, highest))


def sigmoid(x):
    """Return activation value of x with sigmoid function"""
    return 1/(1 + math.exp(-x))


def step(x):
    """Return activation value of x with sign function"""
    return 1 if x >= 0 else 0

try:  # math.isclose was added in Python 3.5
    from math import isclose
except ImportError:
    def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
        "Return true if numbers a and b are close to each other."
        return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

# ______________________________________________________________________________
# Misc Functions


def printf(format_str, *args):
    """Format args with the first argument as format string, and write.
    Return the last arg, or format itself if there are no args."""
    print(str(format_str).format(*args, end=''))

    return args[-1] if args else format_str


def caller(n=1):
    """Return the name of the calling function n levels up
       in the frame stack.
    """
    import inspect

    return inspect.getouterframes(inspect.currentframe())[n][3]

# TODO: Use functools.lru_cache memoization decorator


def memoize(fn, slot=None):
    """Memoize fn: make it remember the computed value for any argument list.
    If slot is specified, store result in that slot of first argument.
    If slot is false, store results in a dictionary."""
    if slot:
        def memoized_fn(obj, *args):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            else:
                val = fn(obj, *args)
                setattr(obj, slot, val)
                return val
    else:
        def memoized_fn(*args):
            if args not in memoized_fn.cache:
                memoized_fn.cache[args] = fn(*args)
            return memoized_fn.cache[args]

        memoized_fn.cache = {}

    return memoized_fn


def name(obj):
    "Try to find some reasonable name for the object."
    return (getattr(obj, 'name', 0) or getattr(obj, '__name__', 0) or
            getattr(getattr(obj, '__class__', 0), '__name__', 0) or
            str(obj))


def isnumber(x):
    "Is x a number? We say it is if it has a __int__ method."
    return hasattr(x, '__int__')


def issequence(x):
    "Is x a sequence? We say it is if it has a __getitem__ method."
    return hasattr(x, '__getitem__')


def print_table(table, header=None, sep='   ', numfmt='%g'):
    """Print a list of lists as a table, so that columns line up nicely.
    header, if specified, will be printed as the first row.
    numfmt is the format for all numbers; you might want e.g. '%6.2f'.
    (If you want different formats in different columns,
    don't use print_table.) sep is the separator between columns."""
    justs = ['rjust' if isnumber(x) else 'ljust' for x in table[0]]

    if header:
        table.insert(0, header)

    table = [[numfmt.format(x) if isnumber(x) else x for x in row]
             for row in table]

    sizes = list(
            map(lambda seq: max(list(map(len, seq))),
                list(zip(*[list(map(str, row)) for row in table]))))

    for row in table:
        print(sep.join(getattr(
            str(x), j)(size) for (j, size, x) in zip(justs, sizes, row)))


def AIMAFile(components, mode='r'):
    "Open a file based at the AIMA root directory."
    aima_root = os.path.dirname(__file__)

    aima_file = os.path.join(aima_root, *components)

    return open(aima_file)


def DataFile(name, mode='r'):
    "Return a file in the AIMA /data directory."
    return AIMAFile(['aima-data', name], mode)


def unimplemented():
    "Use this as a stub for not-yet-implemented functions."
    raise NotImplementedError

# ______________________________________________________________________________
# Queues: Stack, FIFOQueue, PriorityQueue

# TODO: Use queue.Queue


class Queue:

    """Queue is an abstract class/interface. There are three types:
        Stack(): A Last In First Out Queue.
        FIFOQueue(): A First In First Out Queue.
        PriorityQueue(order, f): Queue in sorted order (default min-first).
    Each type supports the following methods and functions:
        q.append(item)  -- add an item to the queue
        q.extend(items) -- equivalent to: for item in items: q.append(item)
        q.pop()         -- return the top item from the queue
        len(q)          -- number of items in q (also q.__len())
        item in q       -- does q contain item?
    Note that isinstance(Stack(), Queue) is false, because we implement stacks
    as lists.  If Python ever gets interfaces, Queue will be an interface."""

    def __init__(self):
        raise NotImplementedError

    def extend(self, items):
        for item in items:
            self.append(item)


def Stack():
    """Return an empty list, suitable as a Last-In-First-Out Queue."""
    return []


class FIFOQueue(Queue):

    """A First-In-First-Out Queue."""

    def __init__(self):
        self.A = []
        self.start = 0

    def append(self, item):
        self.A.append(item)

    def __len__(self):
        return len(self.A) - self.start

    def extend(self, items):
        self.A.extend(items)

    def pop(self):
        e = self.A[self.start]
        self.start += 1
        if self.start > 5 and self.start > len(self.A)/2:
            self.A = self.A[self.start:]
            self.start = 0
        return e

    def __contains__(self, item):
        return item in self.A[self.start:]

# TODO: Use queue.PriorityQueue


class PriorityQueue(Queue):

    """A queue in which the minimum (or maximum) element (as determined by f and
    order) is returned first. If order is min, the item with minimum f(x) is
    returned first; if order is max, then it is the item with maximum f(x).
    Also supports dict-like lookup."""

    def __init__(self, order=min, f=lambda x: x):
        self.A = []
        self.order = order
        self.f = f

    def append(self, item):
        bisect.insort(self.A, (self.f(item), item))

    def __len__(self):
        return len(self.A)

    def pop(self):
        if self.order == min:
            return self.A.pop(0)[1]
        else:
            return self.A.pop()[1]

    def __contains__(self, item):
        return any(item == pair[1] for pair in self.A)

    def __getitem__(self, key):
        for _, item in self.A:
            if item == key:
                return item

    def __delitem__(self, key):
        for i, (value, item) in enumerate(self.A):
            if item == key:
                self.A.pop(i)

# Fig: The idea is we can define things like Fig[3,10] later.
# Alas, it is Fig[3,10] not Fig[3.10], because that would be the same
# as Fig[3.1]
Fig = {}
