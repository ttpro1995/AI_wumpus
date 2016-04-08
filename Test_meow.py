from logic import *

the_kb = PropKB()
A = Expr('A')
B = Expr('B')
notA = Expr('~',A)

X = A | B

the_kb.tell(X)
the_kb.tell(notA)
print(the_kb.ask(A))
the_kb.tell(~B)
print(~B)


anotherKB = PropKB()
C = Expr('C')

D = A & B >> ~C
anotherKB.tell(D)
anotherKB.tell(A)
anotherKB.tell(B)
print(anotherKB.ask(C))