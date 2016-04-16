from logic import *
A = ~Expr("W{}_{}".format(1, 1))
B = ~Expr("W{}_{}".format(1, 1 - 1))
disAB = Expr(A | B)
print(disAB)



