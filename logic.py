"""Representations and Inference for Logic (Chapters 7-9, 12)

Covers both Propositional and First-Order Logic. First we have four
important data types:

    KB            Abstract class holds a knowledge base of logical expressions
    KB_Agent      Abstract class subclasses agents.Agent
    Expr          A logical expression
    substitution  Implemented as a dictionary of var:value pairs, {x:1, y:x}

Be careful: some functions take an Expr as argument, and some take a KB.
Then we implement various functions for doing logical inference:

    pl_true          Evaluate a propositional logical sentence in a model
    tt_entails       Say if a statement is entailed by a KB
    pl_resolution    Do resolution on propositional sentences
    dpll_satisfiable See if a propositional sentence is satisfiable
    WalkSAT          Try to find a solution for a set of clauses

And a few other functions:

    to_cnf           Convert to conjunctive normal form
    unify            Do unification of two FOL sentences
    diff, simp       Symbolic differentiation and simplification
"""

from utils import *  # noqa
import agents
from search import *

import itertools
import re
from collections import defaultdict
import GenerateSentence

# TODO: Fix the precedence of connectives in expr()

# ______________________________________________________________________________


class KB:

    """A knowledge base to which you can tell and ask sentences.
    To create a KB, first subclass this class and implement
    tell, ask_generator, and retract.  Why ask_generator instead of ask?
    The book is a bit vague on what ask means --
    For a Propositional Logic KB, ask(P & Q) returns True or False, but for an
    FOL KB, something like ask(Brother(x, y)) might return many substitutions
    such as {x: Cain, y: Abel}, {x: Abel, y: Cain}, {x: George, y: Jeb}, etc.
    So ask_generator generates these one at a time, and ask either returns the
    first one or returns False."""

    def __init__(self, sentence=None):
        raise NotImplementedError

    def tell(self, sentence):
        "Add the sentence to the KB."
        raise NotImplementedError

    def ask(self, query):
        """Return a substitution that makes the query true, or, failing that, return False."""
        return first(self.ask_generator(query), default=False)

    def ask_generator(self, query):
        "Yield all the substitutions that make query true."
        raise NotImplementedError

    def retract(self, sentence):
        "Remove sentence from the KB."
        raise NotImplementedError


class PropKB(KB):

    "A KB for propositional logic. Inefficient, with no indexing."

    def __init__(self, sentence=None):
        self.clauses = []
        if sentence:
            self.tell(sentence)

    def tell(self, sentence):
        "Add the sentence's clauses to the KB."
        self.clauses.extend(conjuncts(to_cnf(sentence)))

    def ask_generator(self, query):
        "Return the empty substitution {} if KB entails query; else return None."
        if tt_entails(Expr('&', *self.clauses), query):
            yield {}


    def ask_if_true(self, query):
        "Return True if the KB entails query, else return False."
        if self.ask_generator(query) == {}:
            return True
        else:
            return False

    def retract(self, sentence):
        "Remove the sentence's clauses from the KB."
        for c in conjuncts(to_cnf(sentence)):
            if c in self.clauses:
                self.clauses.remove(c)

# ______________________________________________________________________________


def KB_AgentProgram(KB,plan,mapsize):
    """A generic logical knowledge-based agent program. [Fig. 7.1]

    inputs: percept, a list, [stench,breeze,glitter,bump,scream]

    persistent: KB, a knowledge base, initially the atemporal “wumpus physics”
                t, a counter, initially 0, indicating time
                plan, an action sequence, initially empty
    """
    steps = itertools.count()


    def program(percept):
        print("start program with percept ")
        print(percept)
        t = next(steps)
        current = (1, 1)  # current position


        KB.tell(GenerateSentence.genBreezeStenchLogic(mapsize))

        #  if ASK(KB, Glitter t) = true then
        #  plan ← [Grab] + PLAN - ROUTE(current, {[1, 1]}, safe) + [Climb]


        # TELL(KB, MAKE-PERCEPT-SENTENCE(percept, t))
        KB.tell(make_percept_sentence(percept, t))
        safe = []
        unvisited = []

        # safe ← {[x, y] : ASK(KB, OK t x,y) = true}
        for x in range(mapsize):
            for y in range(mapsize):
                if isSafe(x, y, t):
                    safe.append((x, y))  # append safe location to safe list

        # if ASK(KB, Glitter t) = true then

        # unvisited ← {[x, y] : ASK(KB, Lt x,y  ) = false for all t ≤ t}
        if not plan:  # if plan is empty
            for t_prim in range(t + 1):
                for x in range(mapsize):
                    for y in range(mapsize):
                        L_xyt = Expr("L{}_{}_{}".format(x, y, t_prim))
                        r = KB.ask(L_xyt)
                        if r is False:  # don't change "r is False" to "not r", it will not work
                            unvisited.append((x, y))
                        elif t_prim == t:
                            current = (x, y)  # L_xyt is true where t = current time
            # plan ← PLAN-ROUTE(current, unvisited ∩ safe, safe)
            unvisited_safe = []
            for s in safe:
                if s in unvisited:
                    unvisited_safe.append(s)
            new_plan = plan_route(current, unvisited_safe, safe)
            plan.append(new_plan)

        if not plan:
            new_plan = plan_route(current, [(1, 1)], safe)
            plan.append(new_plan)

        return plan.pop()

    def make_percept_sentence(percept, t):
        percepts_list = ['Stench', 'Breeze', 'Glitter', 'Bump', 'Scream']
        axiom = []
        check = [False, False, False, False, False]
        for p in percept:
            p_name = p.__class__.__name__
            for i in range(len(percepts_list)):
                if p_name == percepts_list[i]:
                    check[i] = True;
        for i in range(len(check)):
            if check[i]:
                str_axiom = percepts_list[i] + str(t)
                axiom.append(Expr(str_axiom))
            else:
                str_axiom = percepts_list[i] + str(t)
                axiom.append(~Expr(str_axiom))

        conj = conj_axiom_list(axiom)
        return conj

    def isSafe(x, y, t):
        OK_xyt = Expr('OK{}_{}_{}'.format(x, y, t))
        r = KB.ask(OK_xyt)
        if r is not False:  # ask return {}, but {} is not True also
            return True
        else:
            return False  # ask return False when the logic false
        return r


    def make_action_query(t):
        pass

    def make_action_sentence(action, t):
        pass

    return program



class Expr:

    """A symbolic mathematical expression.  We use this class for logical
    expressions, and for terms within logical expressions. In general, an
    Expr has an op (operator) and a list of args.  The op can be:
      Null-ary (no args) op:
        A number, representing the number itself.  (e.g. Expr(42) => 42)
        A symbol, representing a variable or constant (e.g. Expr('F') => F)
      Unary (1 arg) op:
        '~', '-', representing NOT, negation (e.g. Expr('~', Expr('P')) => ~P)
      Binary (2 arg) op:
        '>>', '<<', representing forward and backward implication
        '+', '-', '*', '/', '**', representing arithmetic operators
        '<', '>', '>=', '<=', representing comparison operators
        '<=>', '^', representing logical equality and XOR
      N-ary (0 or more args) op:
        '&', '|', representing conjunction and disjunction
        A symbol, representing a function term or FOL proposition

    Exprs can be constructed with operator overloading: if x and y are Exprs,
    then so are x + y and x & y, etc.  Also, if F and x are Exprs, then so is
    F(x); it works by overloading the __call__ method of the Expr F.  Note
    that in the Expr that is created by F(x), the op is the str 'F', not the
    Expr F.   See http://www.python.org/doc/current/ref/specialnames.html
    to learn more about operator overloading in Python.

    WARNING: x == y and x != y are NOT Exprs.  The reason is that we want
    to write code that tests 'if x == y:' and if x == y were the same
    as Expr('==', x, y), then the result would always be true; not what a
    programmer would expect.  But we still need to form Exprs representing
    equalities and disequalities.  We concentrate on logical equality (or
    equivalence) and logical disequality (or XOR).  You have 3 choices:
        (1) Expr('<=>', x, y) and Expr('^', x, y)
            Note that ^ is bitwise XOR in Python (and Java and C++)
        (2) expr('x <=> y') and expr('x =/= y').
            See the doc string for the function expr.
        (3) (x % y) and (x ^ y).
            It is very ugly to have (x % y) mean (x <=> y), but we need
            SOME operator to make (2) work, and this seems the best choice.
    """

    def __init__(self, op, *args):
        "op is a string or number; args are Exprs (or are coerced to Exprs)."
        assert isinstance(op, str) or (isnumber(op) and not args)
        self.op = num_or_str(op)
        self.args = list(map(expr, args))  # Coerce args to Exprs

    def __call__(self, *args):
        """Self must be a symbol with no args, such as Expr('F').  Create a new
        Expr with 'F' as op and the args as arguments."""
        assert is_symbol(self.op) and not self.args
        return Expr(self.op, *args)

    def __repr__(self):
        "Show something like 'P' or 'P(x, y)', or '~P' or '(P | Q | R)'"
        if not self.args:         # Constant or proposition with arity 0
            return str(self.op)
        elif is_symbol(self.op):  # Functional or propositional operator
            return '{}({})'.format(self.op, ', '.join(map(repr, self.args)))
        elif len(self.args) == 1:  # Prefix operator
            return self.op + repr(self.args[0])
        else:                     # Infix operator
            return '({})'.format((' '+self.op+' ').join(map(repr, self.args)))

    def __eq__(self, other):
        """x and y are equal iff their ops and args are equal."""
        return (other is self) or (isinstance(other, Expr) and
                                   self.op == other.op and
                                   self.args == other.args)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        "Need a hash method so Exprs can live in dicts."
        return hash(self.op) ^ hash(tuple(self.args))

    # See http://www.python.org/doc/current/lib/module-operator.html
    # Not implemented: not, abs, pos, concat, contains, *item, *slice
    def __lt__(self, other): return Expr('<',  self, other)

    def __le__(self, other): return Expr('<=', self, other)

    def __ge__(self, other): return Expr('>=', self, other)

    def __gt__(self, other): return Expr('>',  self, other)

    def __add__(self, other): return Expr('+',  self, other)

    def __radd__(self, other): return Expr('+', other, self)

    def __sub__(self, other): return Expr('-',  self, other)

    def __rsub__(self, other): return Expr('-',  other, self)

    def __and__(self, other): return Expr('&',  self, other)

    def __div__(self, other): return Expr('/',  self, other)

    def __truediv__(self, other): return Expr('/',  self, other)

    def __invert__(self): return Expr('~',  self)

    def __lshift__(self, other): return Expr('<<', self, other)

    def __rshift__(self, other): return Expr('>>', self, other)

    def __mul__(self, other): return Expr('*',  self, other)

    def __neg__(self): return Expr('-',  self)

    def __or__(self, other): return Expr('|',  self, other)

    def __pow__(self, other): return Expr('**', self, other)

    def __xor__(self, other): return Expr('^',  self, other)

    def __mod__(self, other): return Expr('<=>',  self, other)


def expr(s):
    """Create an Expr representing a logic expression by parsing the input
    string. Symbols and numbers are automatically converted to Exprs.
    In addition you can use alternative spellings of these operators:
      'x ==> y'   parses as   (x >> y)    # Implication
      'x <== y'   parses as   (x << y)    # Reverse implication
      'x <=> y'   parses as   (x % y)     # Logical equivalence
      'x =/= y'   parses as   (x ^ y)     # Logical disequality (xor)
    But BE CAREFUL; precedence of implication is wrong. expr('P & Q ==> R & S')
    is ((P & (Q >> R)) & S); so you must use expr('(P & Q) ==> (R & S)').
    """
    if isinstance(s, Expr):
        return s
    if isnumber(s):
        return Expr(s)
    # Replace the alternative spellings of operators with canonical spellings
    s = s.replace('==>', '>>').replace('<==', '<<')
    s = s.replace('<=>', '%').replace('=/=', '^')
    # Replace a symbol or number, such as 'P' with 'Expr("P")'
    s = re.sub(r'([a-zA-Z0-9_.]+)', r'Expr("\1")', s)
    # Now eval the string.  (A security hole; do not use with an adversary.)
    return eval(s, {'Expr': Expr})


def is_symbol(s):
    "A string s is a symbol if it starts with an alphabetic char."
    return isinstance(s, str) and s[:1].isalpha()


def is_var_symbol(s):
    "A logic variable symbol is an initial-lowercase string."
    return is_symbol(s) and s[0].islower()


def is_prop_symbol(s):
    """A proposition logic symbol is an initial-uppercase string other than
    TRUE or FALSE."""
    return is_symbol(s) and s[0].isupper() and s != 'TRUE' and s != 'FALSE'


def variables(s):
    """Return a set of the variables in expression s.
    >>> variables(expr('F(x, x) & G(x, y) & H(y, z) & R(A, z, z)')) == {x, y, z}
    True
    """
    result = set([])

    def walk(s):
        if is_variable(s):
            result.add(s)
        else:
            for arg in s.args:
                walk(arg)
    walk(s)
    return result


def is_definite_clause(s):
    """returns True for exprs s of the form A & B & ... & C ==> D,
    where all literals are positive.  In clause form, this is
    ~A | ~B | ... | ~C | D, where exactly one clause is positive.
    >>> is_definite_clause(expr('Farmer(Mac)'))
    True
    """
    if is_symbol(s.op):
        return True
    elif s.op == '>>':
        antecedent, consequent = s.args
        return (is_symbol(consequent.op) and
                every(lambda arg: is_symbol(arg.op), conjuncts(antecedent)))
    else:
        return False


def parse_definite_clause(s):
    "Return the antecedents and the consequent of a definite clause."
    assert is_definite_clause(s)
    if is_symbol(s.op):
        return [], s
    else:
        antecedent, consequent = s.args
        return conjuncts(antecedent), consequent

# Useful constant Exprs used in examples and code:
TRUE, FALSE = Expr('TRUE'), Expr('FALSE')
ZERO, ONE, TWO = 0, 1, 2
A, B, C, D, E, F, G, P, Q, x, y, z = map(Expr, 'ABCDEFGPQxyz')

# ______________________________________________________________________________


def tt_entails(kb, alpha):
    """Does kb entail the sentence alpha? Use truth tables. For propositional
    kb's and sentences. [Fig. 7.10]. Note that the 'kb' should be an
    Expr which is a conjunction of clauses.
    >>> tt_entails(expr('P & Q'), expr('Q'))
    True
    """
    assert not variables(alpha)
    return tt_check_all(kb, alpha, prop_symbols(kb & alpha), {})


def tt_check_all(kb, alpha, symbols, model):
    "Auxiliary routine to implement tt_entails."
    if not symbols:
        if pl_true(kb, model):
            result = pl_true(alpha, model)
            assert result in (True, False)
            return result
        else:
            return True
    else:
        P, rest = symbols[0], symbols[1:]
        return (tt_check_all(kb, alpha, rest, extend(model, P, True)) and
                tt_check_all(kb, alpha, rest, extend(model, P, False)))


def prop_symbols(x):
    "Return a list of all propositional symbols in x."
    if not isinstance(x, Expr):
        return []
    elif is_prop_symbol(x.op):
        return [x]
    else:
        return list(set(symbol for arg in x.args for symbol in prop_symbols(arg)))


def tt_true(alpha):
    """Is the propositional sentence alpha a tautology? (alpha will be
    coerced to an expr.)
    >>> tt_true(expr("(P >> Q) <=> (~P | Q)"))
    True
    """
    return tt_entails(TRUE, expr(alpha))


def pl_true(exp, model={}):
    """Return True if the propositional logic expression is true in the model,
    and False if it is false. If the model does not specify the value for
    every proposition, this may return None to indicate 'not obvious';
    this may happen even when the expression is tautological."""
    op, args = exp.op, exp.args
    if exp == TRUE:
        return True
    elif exp == FALSE:
        return False
    elif is_prop_symbol(op):
        return model.get(exp)
    elif op == '~':
        p = pl_true(args[0], model)
        if p is None:
            return None
        else:
            return not p
    elif op == '|':
        result = False
        for arg in args:
            p = pl_true(arg, model)
            if p is True:
                return True
            if p is None:
                result = None
        return result
    elif op == '&':
        result = True
        for arg in args:
            p = pl_true(arg, model)
            if p is False:
                return False
            if p is None:
                result = None
        return result
    p, q = args
    if op == '>>':
        return pl_true(~p | q, model)
    elif op == '<<':
        return pl_true(p | ~q, model)
    pt = pl_true(p, model)
    if pt is None:
        return None
    qt = pl_true(q, model)
    if qt is None:
        return None
    if op == '<=>':
        return pt == qt
    elif op == '^':
        return pt != qt
    else:
        raise ValueError("illegal operator in logic expression" + str(exp))

# ______________________________________________________________________________

# Convert to Conjunctive Normal Form (CNF)


def to_cnf(s):
    """Convert a propositional logical sentence s to conjunctive normal form.
    That is, to the form ((A | ~B | ...) & (B | C | ...) & ...) [p. 253]
    >>> to_cnf("~(B|C)")
    (~B & ~C)
    """
    if isinstance(s, str):
        s = expr(s)
    s = eliminate_implications(s)  # Steps 1, 2 from p. 253
    s = move_not_inwards(s)  # Step 3
    return distribute_and_over_or(s)  # Step 4


def eliminate_implications(s):
    "Change implications into equivalent form with only &, |, and ~ as logical operators."
    if not s.args or is_symbol(s.op):
        return s  # Atoms are unchanged.
    args = list(map(eliminate_implications, s.args))
    a, b = args[0], args[-1]
    if s.op == '>>' or s.op == '==>':
        return (b | ~a)
    elif s.op == '<<' or s.op == '<==':
        return (a | ~b)
    elif s.op == '<=>':
        return (a | ~b) & (b | ~a)
    elif s.op == '^' or s.op == '<=/=>':
        assert len(args) == 2  # TODO: relax this restriction
        return (a & ~b) | (~a & b)
    else:
        assert s.op in ('&', '|', '~')
        return Expr(s.op, *args)


def move_not_inwards(s):
    """Rewrite sentence s by moving negation sign inward.
    >>> move_not_inwards(~(A | B))
    (~A & ~B)"""
    if s.op == '~':
        def NOT(b): return move_not_inwards(~b)  # noqa
        a = s.args[0]
        if a.op == '~':
            return move_not_inwards(a.args[0])  # ~~A ==> A
        if a.op == '&':
            return associate('|', list(map(NOT, a.args)))
        if a.op == '|':
            return associate('&', list(map(NOT, a.args)))
        return s
    elif is_symbol(s.op) or not s.args:
        return s
    else:
        return Expr(s.op, *list(map(move_not_inwards, s.args)))


def distribute_and_over_or(s):
    """Given a sentence s consisting of conjunctions and disjunctions
    of literals, return an equivalent sentence in CNF.
    >>> distribute_and_over_or((A & B) | C)
    ((A | C) & (B | C))
    """
    if s.op == '|':
        s = associate('|', s.args)
        if s.op != '|':
            return distribute_and_over_or(s)
        if len(s.args) == 0:
            return FALSE
        if len(s.args) == 1:
            return distribute_and_over_or(s.args[0])
        conj = first(arg for arg in s.args if arg.op == '&')
        if not conj:
            return s
        others = [a for a in s.args if a is not conj]
        rest = associate('|', others)
        return associate('&', [distribute_and_over_or(c | rest)
                               for c in conj.args])
    elif s.op == '&':
        return associate('&', list(map(distribute_and_over_or, s.args)))
    else:
        return s


def associate(op, args):
    """Given an associative op, return an expression with the same
    meaning as Expr(op, *args), but flattened -- that is, with nested
    instances of the same op promoted to the top level.
    >>> associate('&', [(A&B),(B|C),(B&C)])
    (A & B & (B | C) & B & C)
    >>> associate('|', [A|(B|(C|(A&B)))])
    (A | B | C | (A & B))
    """
    args = dissociate(op, args)
    if len(args) == 0:
        return _op_identity[op]
    elif len(args) == 1:
        return args[0]
    else:
        return Expr(op, *args)

_op_identity = {'&': TRUE, '|': FALSE, '+': ZERO, '*': ONE}


def dissociate(op, args):
    """Given an associative op, return a flattened list result such
    that Expr(op, *result) means the same as Expr(op, *args)."""
    result = []

    def collect(subargs):
        for arg in subargs:
            if arg.op == op:
                collect(arg.args)
            else:
                result.append(arg)
    collect(args)
    return result


def conjuncts(s):
    """Return a list of the conjuncts in the sentence s.
    >>> conjuncts(A & B)
    [A, B]
    >>> conjuncts(A | B)
    [(A | B)]
    """
    return dissociate('&', [s])


def disjuncts(s):
    """Return a list of the disjuncts in the sentence s.
    >>> disjuncts(A | B)
    [A, B]
    >>> disjuncts(A & B)
    [(A & B)]
    """
    return dissociate('|', [s])

# ______________________________________________________________________________


def pl_resolution(KB, alpha):
    "Propositional-logic resolution: say if alpha follows from KB. [Fig. 7.12]"
    clauses = KB.clauses + conjuncts(to_cnf(~alpha))
    new = set()
    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j])
                 for i in range(n) for j in range(i+1, n)]
        for (ci, cj) in pairs:
            resolvents = pl_resolve(ci, cj)
            if FALSE in resolvents:
                return True
            new = new.union(set(resolvents))
        if new.issubset(set(clauses)):
            return False
        for c in new:
            if c not in clauses:
                clauses.append(c)


def pl_resolve(ci, cj):
    """Return all clauses that can be obtained by resolving clauses ci and cj."""
    clauses = []
    for di in disjuncts(ci):
        for dj in disjuncts(cj):
            if di == ~dj or ~di == dj:
                dnew = unique(removeall(di, disjuncts(ci)) +
                              removeall(dj, disjuncts(cj)))
                clauses.append(associate('|', dnew))
    return clauses

# ______________________________________________________________________________


class PropDefiniteKB(PropKB):

    "A KB of propositional definite clauses."

    def tell(self, sentence):
        "Add a definite clause to this KB."
        assert is_definite_clause(sentence), "Must be definite clause"
        self.clauses.append(sentence)

    def ask_generator(self, query):
        "Yield the empty substitution if KB implies query; else nothing."
        if pl_fc_entails(self.clauses, query):
            yield {}

    def retract(self, sentence):
        self.clauses.remove(sentence)

    def clauses_with_premise(self, p):
        """Return a list of the clauses in KB that have p in their premise.
        This could be cached away for O(1) speed, but we'll recompute it."""
        return [c for c in self.clauses
                if c.op == '>>' and p in conjuncts(c.args[0])]


def pl_fc_entails(KB, q):
    """Use forward chaining to see if a PropDefiniteKB entails symbol q.
    [Fig. 7.15]
    >>> pl_fc_entails(Fig[7,15], expr('Q'))
    True
    """
    count = dict([(c, len(conjuncts(c.args[0]))) for c in KB.clauses
                  if c.op == '>>'])
    inferred = defaultdict(bool)
    agenda = [s for s in KB.clauses if is_prop_symbol(s.op)]
    while agenda:
        p = agenda.pop()
        if p == q:
            return True
        if not inferred[p]:
            inferred[p] = True
            for c in KB.clauses_with_premise(p):
                count[c] -= 1
                if count[c] == 0:
                    agenda.append(c.args[1])
    return False

# Wumpus World example [Fig. 7.13]
Fig[7, 13] = expr("(B11 <=> (P12 | P21))  &  ~B11")

# Propositional Logic Forward Chaining example [Fig. 7.16]
Fig[7, 15] = PropDefiniteKB()
for s in "P>>Q   (L&M)>>P   (B&L)>>M   (A&P)>>L   (A&B)>>L   A   B".split():
    Fig[7, 15].tell(expr(s))

# ______________________________________________________________________________
# DPLL-Satisfiable [Fig. 7.17]


def dpll_satisfiable(s):
    """Check satisfiability of a propositional sentence.
    This differs from the book code in two ways: (1) it returns a model
    rather than True when it succeeds; this is more useful. (2) The
    function find_pure_symbol is passed a list of unknown clauses, rather
    than a list of all clauses and the model; this is more efficient."""
    clauses = conjuncts(to_cnf(s))
    symbols = prop_symbols(s)
    return dpll(clauses, symbols, {})


def dpll(clauses, symbols, model):
    "See if the clauses are true in a partial model."
    unknown_clauses = []  # clauses with an unknown truth value
    for c in clauses:
        val = pl_true(c, model)
        if val is False:
            return False
        if val is not True:
            unknown_clauses.append(c)
    if not unknown_clauses:
        return model
    P, value = find_pure_symbol(symbols, unknown_clauses)
    if P:
        return dpll(clauses, removeall(P, symbols), extend(model, P, value))
    P, value = find_unit_clause(clauses, model)
    if P:
        return dpll(clauses, removeall(P, symbols), extend(model, P, value))
    if not symbols:
        raise TypeError("Argument should be of the type Expr.")
    P, symbols = symbols[0], symbols[1:]
    return (dpll(clauses, symbols, extend(model, P, True)) or
            dpll(clauses, symbols, extend(model, P, False)))


def find_pure_symbol(symbols, clauses):
    """Find a symbol and its value if it appears only as a positive literal
    (or only as a negative) in clauses.
    >>> find_pure_symbol([A, B, C], [A|~B,~B|~C,C|A])
    (A, True)
    """
    for s in symbols:
        found_pos, found_neg = False, False
        for c in clauses:
            if not found_pos and s in disjuncts(c):
                found_pos = True
            if not found_neg and ~s in disjuncts(c):
                found_neg = True
        if found_pos != found_neg:
            return s, found_pos
    return None, None


def find_unit_clause(clauses, model):
    """Find a forced assignment if possible from a clause with only 1
    variable not bound in the model.
    >>> find_unit_clause([A|B|C, B|~C, ~A|~B], {A:True})
    (B, False)
    """
    for clause in clauses:
        P, value = unit_clause_assign(clause, model)
        if P:
            return P, value
    return None, None


def unit_clause_assign(clause, model):
    """Return a single variable/value pair that makes clause true in
    the model, if possible.
    >>> unit_clause_assign(A|B|C, {A:True})
    (None, None)
    >>> unit_clause_assign(B|~C, {A:True})
    (None, None)
    >>> unit_clause_assign(~A|~B, {A:True})
    (B, False)
    """
    P, value = None, None
    for literal in disjuncts(clause):
        sym, positive = inspect_literal(literal)
        if sym in model:
            if model[sym] == positive:
                return None, None  # clause already True
        elif P:
            return None, None      # more than 1 unbound variable
        else:
            P, value = sym, positive
    return P, value


def inspect_literal(literal):
    """The symbol in this literal, and the value it should take to
    make the literal true.
    >>> inspect_literal(P)
    (P, True)
    >>> inspect_literal(~P)
    (P, False)
    """
    if literal.op == '~':
        return literal.args[0], False
    else:
        return literal, True

# ______________________________________________________________________________
# Walk-SAT [Fig. 7.18]


def WalkSAT(clauses, p=0.5, max_flips=10000):
    """Checks for satisfiability of all clauses by randomly flipping values of variables
    """
    # set of all symbols in all clauses
    symbols = set(sym for clause in clauses for sym in prop_symbols(clause))
    # model is a random assignment of true/false to the symbols in clauses
    model = dict([(s, random.choice([True, False])) for s in symbols])
    for i in range(max_flips):
        satisfied, unsatisfied = [], []
        for clause in clauses:
            (satisfied if pl_true(clause, model) else unsatisfied).append(clause)
        if not unsatisfied:  # if model satisfies all the clauses
            return model
        clause = random.choice(unsatisfied)
        if probability(p):
            sym = random.choice(prop_symbols(clause))
        else:
            # Flip the symbol in clause that maximizes number of sat. clauses
            def sat_count(sym):
                #returns the the number of clauses satisfied after flipping the symbol
                model[sym] = not model[sym]
                count = len([clause for clause in clauses if pl_true(clause, model)])
                model[sym] = not model[sym]
                return count
            sym = argmax(prop_symbols(clause), key=sat_count)
        model[sym] = not model[sym]
    #If no solution is found within the flip limit, we return failure
    return None

# ______________________________________________________________________________
#
#
# class HybridWumpusAgent(agents.Agent):
#
#     "An agent for the wumpus world that does logical inference. [Fig. 7.20]"""
#
#     def __init__(self, mapsize):
#         self.kb = PropKB()
#         self.mapsize = mapsize
#         self.timecounter = 0;
#         bs_logic = GenerateSentence.genBreezeStenchLogic(self.mapsize)
#         one_wumpus_logic = GenerateSentence.genOneWumpusExistLogic(self.mapsize)
#         self.kb.tell(bs_logic)
#         self.kb.tell(one_wumpus_logic)
#         self.plan = []
#
#
#
#
#
#     def step(self, percept):
#         current = (1,1) # current position
#         self.timecounter += 1
#         self.kb.tell(self.make_percept_sentence(percept,self.timecounter))
#         safe = []
#         unvisited = []
#         for x in range(self.mapsize):
#             for y in range(self.mapsize):
#                 if self.isSafe(x,y):
#                     safe.append((x,y)) # append safe location to safe list
#
#         # if ASK(KB, Glitter t) = true then
#
#         # unvisited ← {[x, y] : ASK(KB, Lt x,y  ) = false for all t ≤ t}
#         if not self.plan: # if plan is empty
#             for t_prim in range(self.timecounter+1):
#                 for x in range(self.mapsize):
#                      for y in range(self.mapsize):
#                         L_xyt = Expr("L{}_{}_{}".format(x, y, t_prim))
#                         r = self.kb.ask(L_xyt)
#                         if r is False: # don't change "r is False" to "not r", it will not work
#                             unvisited.append((x, y))
#                         elif t_prim == self.timecounter:
#                             current = (x,y)  # L_xyt is true where t = current time
#             # plan ← PLAN-ROUTE(current, unvisited ∩ safe, safe)
#             unvisited_safe = []
#             for s in safe:
#                 if s in unvisited:
#                     unvisited_safe.append(s)
#             new_plan = plan_route(current,unvisited_safe,safe)
#             self.plan.append(new_plan)
#
#         if not self.plan:
#             new_plan = plan_route(current,[(1,1)],safe)
#             self.plan.append(new_plan)
#
#         return self.plan.pop()
#
    #
    #
    #
    # def make_percept_sentence(percept, t):
    #     percepts_list = ['Stench', 'Breeze', 'Glitter', 'Bump', 'Scream']
    #     axiom = []
    #     check = [False,False,False,False,False]
    #     for p in percept:
    #         p_name = p.__class__.__name__
    #         for i in range(len(percepts_list)):
    #             if p_name == percepts_list[i]:
    #                 check[i] = True;
    #     for i in range(len(check)):
    #         if check[i]:
    #             str_axiom = percepts_list[i]+str(t)
    #             axiom.append(Expr(str_axiom))
    #         else:
    #             str_axiom = percepts_list[i]+str(t)
    #             axiom.append(~Expr(str_axiom))
    #
    #     conj = conj_axiom_list(axiom)
    #     return conj
    #
    # def isSafe(self,x,y):
    #     OK_xyt = Expr('OK{}_{}_{}'.format(x, y, self.timecounter))
    #     r = self.kb.ask(OK_xyt)
    #     if r is not False: # ask return {}, but {} is not True also
    #         return True
    #     else:
    #         return False  # ask return False when the logic false
    #     return r



def plan_route(current, goals, allowed):
    problem = RouteProblem(current,goals,allowed)
    ret = aStarSearch(problem)
    return ret

# ______________________________________________________________________________


def SAT_plan(init, transition, goal, t_max, SAT_solver=dpll_satisfiable):
    "[Fig. 7.22]"
    for t in range(t_max):
        cnf = translate_to_SAT(init, transition, goal, t)
        model = SAT_solver(cnf)
        if model is not False:
            return extract_solution(model)
    return None


def translate_to_SAT(init, transition, goal, t):
    unimplemented()


def extract_solution(model):
    unimplemented()

# ______________________________________________________________________________


def unify(x, y, s):
    """Unify expressions x,y with substitution s; return a substitution that
    would make x,y equal, or None if x,y can not unify. x and y can be
    variables (e.g. Expr('x')), constants, lists, or Exprs. [Fig. 9.1]"""
    if s is None:
        return None
    elif x == y:
        return s
    elif is_variable(x):
        return unify_var(x, y, s)
    elif is_variable(y):
        return unify_var(y, x, s)
    elif isinstance(x, Expr) and isinstance(y, Expr):
        return unify(x.args, y.args, unify(x.op, y.op, s))
    elif isinstance(x, str) or isinstance(y, str):
        return None
    elif issequence(x) and issequence(y) and len(x) == len(y):
        if not x:
            return s
        return unify(x[1:], y[1:], unify(x[0], y[0], s))
    else:
        return None


def is_variable(x):
    "A variable is an Expr with no args and a lowercase symbol as the op."
    return isinstance(x, Expr) and not x.args and is_var_symbol(x.op)


def unify_var(var, x, s):
    if var in s:
        return unify(s[var], x, s)
    elif occur_check(var, x, s):
        return None
    else:
        return extend(s, var, x)


def occur_check(var, x, s):
    """Return true if variable var occurs anywhere in x
    (or in subst(s, x), if s has a binding for x)."""
    if var == x:
        return True
    elif is_variable(x) and x in s:
        return occur_check(var, s[x], s)
    elif isinstance(x, Expr):
        return (occur_check(var, x.op, s) or
                occur_check(var, x.args, s))
    elif isinstance(x, (list, tuple)):
        return first(e for e in x if occur_check(var, e, s))
    else:
        return False


def extend(s, var, val):
    "Copy the substitution s and extend it by setting var to val; return copy."
    s2 = s.copy()
    s2[var] = val
    return s2


def subst(s, x):
    """Substitute the substitution s into the expression x.
    >>> subst({x: 42, y:0}, F(x) + y)
    (F(42) + 0)
    """
    if isinstance(x, list):
        return [subst(s, xi) for xi in x]
    elif isinstance(x, tuple):
        return tuple([subst(s, xi) for xi in x])
    elif not isinstance(x, Expr):
        return x
    elif is_var_symbol(x.op):
        return s.get(x, x)
    else:
        return Expr(x.op, *[subst(s, arg) for arg in x.args])


def fol_fc_ask(KB, alpha):
    unimplemented()


def standardize_variables(sentence, dic=None):
    """Replace all the variables in sentence with new variables."""
    if dic is None:
        dic = {}
    if not isinstance(sentence, Expr):
        return sentence
    elif is_var_symbol(sentence.op):
        if sentence in dic:
            return dic[sentence]
        else:
            v = Expr('v_{}'.format(next(standardize_variables.counter)))
            dic[sentence] = v
            return v
    else:
        return Expr(sentence.op,
                    *[standardize_variables(a, dic) for a in sentence.args])

standardize_variables.counter = itertools.count()

# ______________________________________________________________________________


class FolKB(KB):

    """A knowledge base consisting of first-order definite clauses.
    >>> kb0 = FolKB([expr('Farmer(Mac)'), expr('Rabbit(Pete)'),
    ...              expr('(Rabbit(r) & Farmer(f)) ==> Hates(f, r)')])
    >>> kb0.tell(expr('Rabbit(Flopsie)'))
    >>> kb0.retract(expr('Rabbit(Pete)'))
    >>> kb0.ask(expr('Hates(Mac, x)'))[x]
    Flopsie
    >>> kb0.ask(expr('Wife(Pete, x)'))
    False
    """

    def __init__(self, initial_clauses=[]):
        self.clauses = []  # inefficient: no indexing
        for clause in initial_clauses:
            self.tell(clause)

    def tell(self, sentence):
        if is_definite_clause(sentence):
            self.clauses.append(sentence)
        else:
            raise Exception("Not a definite clause: {}".format(sentence))

    def ask_generator(self, query):
        return fol_bc_ask(self, query)

    def retract(self, sentence):
        self.clauses.remove(sentence)

    def fetch_rules_for_goal(self, goal):
        return self.clauses


test_kb = FolKB(
    list(map(expr, ['Farmer(Mac)',
                    'Rabbit(Pete)',
                    'Mother(MrsMac, Mac)',
                    'Mother(MrsRabbit, Pete)',
                    '(Rabbit(r) & Farmer(f)) ==> Hates(f, r)',
                    '(Mother(m, c)) ==> Loves(m, c)',
                    '(Mother(m, r) & Rabbit(r)) ==> Rabbit(m)',
                    '(Farmer(f)) ==> Human(f)',
                    # Note that this order of conjuncts
                    # would result in infinite recursion:
                    # '(Human(h) & Mother(m, h)) ==> Human(m)'
                    '(Mother(m, h) & Human(h)) ==> Human(m)'
                    ]))
)

crime_kb = FolKB(
    list(map(expr,
             ['(American(x) & Weapon(y) & Sells(x, y, z) & Hostile(z)) ==> Criminal(x)',  # noqa
              'Owns(Nono, M1)',
              'Missile(M1)',
              '(Missile(x) & Owns(Nono, x)) ==> Sells(West, x, Nono)',
              'Missile(x) ==> Weapon(x)',
              'Enemy(x, America) ==> Hostile(x)',
              'American(West)',
              'Enemy(Nono, America)'
              ]))
)


def fol_bc_ask(KB, query):
    """A simple backward-chaining algorithm for first-order logic. [Fig. 9.6]
    KB should be an instance of FolKB, and query an atomic sentence. """
    return fol_bc_or(KB, query, {})


def fol_bc_or(KB, goal, theta):
    for rule in KB.fetch_rules_for_goal(goal):
        lhs, rhs = parse_definite_clause(standardize_variables(rule))
        for theta1 in fol_bc_and(KB, lhs, unify(rhs, goal, theta)):
            yield theta1


def fol_bc_and(KB, goals, theta):
    if theta is None:
        pass
    elif not goals:
        yield theta
    else:
        first, rest = goals[0], goals[1:]
        for theta1 in fol_bc_or(KB, subst(theta, first), theta):
            for theta2 in fol_bc_and(KB, rest, theta1):
                yield theta2

# ______________________________________________________________________________

# Example application (not in the book).
# You can use the Expr class to do symbolic differentiation.  This used to be
# a part of AI; now it is considered a separate field, Symbolic Algebra.


def diff(y, x):
    """Return the symbolic derivative, dy/dx, as an Expr.
    However, you probably want to simplify the results with simp.
    >>> diff(x * x, x)
    ((x * 1) + (x * 1))
    """
    if y == x:
        return ONE
    elif not y.args:
        return ZERO
    else:
        u, op, v = y.args[0], y.op, y.args[-1]
        if op == '+':
            return diff(u, x) + diff(v, x)
        elif op == '-' and len(args) == 1:
            return -diff(u, x)
        elif op == '-':
            return diff(u, x) - diff(v, x)
        elif op == '*':
            return u * diff(v, x) + v * diff(u, x)
        elif op == '/':
            return (v*diff(u, x) - u*diff(v, x)) / (v * v)
        elif op == '**' and isnumber(x.op):
            return (v * u ** (v - 1) * diff(u, x))
        elif op == '**':
            return (v * u ** (v - 1) * diff(u, x) +
                    u ** v * Expr('log')(u) * diff(v, x))
        elif op == 'log':
            return diff(u, x) / u
        else:
            raise ValueError("Unknown op: {} in diff({}, {})".format(op, y, x))


def simp(x):
    "Simplify the expression x."
    if not x.args:
        return x
    args = list(map(simp, x.args))
    u, op, v = args[0], x.op, args[-1]
    if op == '+':
        if v == ZERO:
            return u
        if u == ZERO:
            return v
        if u == v:
            return TWO * u
        if u == -v or v == -u:
            return ZERO
    elif op == '-' and len(args) == 1:
        if u.op == '-' and len(u.args) == 1:
            return u.args[0]  # --y ==> y
    elif op == '-':
        if v == ZERO:
            return u
        if u == ZERO:
            return -v
        if u == v:
            return ZERO
        if u == -v or v == -u:
            return ZERO
    elif op == '*':
        if u == ZERO or v == ZERO:
            return ZERO
        if u == ONE:
            return v
        if v == ONE:
            return u
        if u == v:
            return u ** 2
    elif op == '/':
        if u == ZERO:
            return ZERO
        if v == ZERO:
            return Expr('Undefined')
        if u == v:
            return ONE
        if u == -v or v == -u:
            return ZERO
    elif op == '**':
        if u == ZERO:
            return ZERO
        if v == ZERO:
            return ONE
        if u == ONE:
            return ONE
        if v == ONE:
            return u
    elif op == 'log':
        if u == ONE:
            return ZERO
    else:
        raise ValueError("Unknown op: " + op)
    # If we fall through to here, we can not simplify further
    return Expr(op, *args)


def d(y, x):
    "Differentiate and then simplify."
    return simp(diff(y, x))

# _________________________________________________________________________

# Utilities for doctest cases
# These functions print their arguments in a standard order
# to compensate for the random order in the standard representation

'''
conjunction and disjunction list

example
l.append(Expr('A'))
l.append(Expr('D'))
l.append(Expr('C'))
l.append(Expr('B'))

E = conj_axiom_list(l)
print(E)
'''
def conj_axiom_list(axiom_list):
    r = axiom_list[0]
    for a in axiom_list:
        if a is not r:
            r = r & a
    return  r

def disj_axiom_list(axiom_list):
    r = axiom_list[0]
    for a in axiom_list:
        if a is not r:
            r = r | a
    return  r



# ________________________________________________________________________

