from logic import *
#
# # the_kb = PropKB()
# # A = Expr('A')
# # B = Expr('B')
# # notA = Expr('~',A)
# #
# # X = A | B
# #
# # the_kb.tell(X)
# # the_kb.tell(notA)
# # print(the_kb.ask(A))
# # the_kb.tell(~B)
# # print(~B)
# #
# #
# # anotherKB = PropKB()
# # C = Expr('C')
# #
# # D = A & B >> ~C
# # anotherKB.tell(D)
# # anotherKB.tell(A)
# # anotherKB.tell(B)
# # print(anotherKB.ask(C))
#
# # meow_kb = PropKB()
# # A = Expr('A')
# # B = Expr('B')
# # C = Expr('C')
# # D = A & B >> C
# # E = Expr('E')
# # F = Expr('F')
# #
# # meow_kb.tell(A) # A
# # meow_kb.tell(B) # B
# # meow_kb.tell(D) # A & B >> C
# # meow_kb.tell(~E) # ~ E
# # print(meow_kb.ask(C))
# # print(meow_kb.ask(E))
# # print(meow_kb.ask(F))
# #
# # A = Expr('A')
# # B = Expr('B')
# # C = Expr('C')
# # D = A | B
# # m_kb = PropKB()
# # m_kb.tell(D) # A | B
# # m_kb.tell(~A)
# # print(m_kb.ask(B))
#
# #OK_xyt % ~P_xy & ~(Wxy & WumpusAlive_t)
#
# # A = Expr(OK_xyt % ~P_xy & ~(Wxy & WumpusAlive_t))
# # B= Expr("~P_xy & ~(Wxy & WumpusAlive_t)")
# import re
# my_pat = r"[a-zA-Z0-9]"
# OK_xyt = Expr("OK_xyt")
# P_xy = Expr("P_xy")
# Wxy = Expr("Wxy")
# WumpusAlive_t = Expr("WumpusAlive_t")
# A = K_xyt % (~P_xy & ~(Wxy & WumpusAlive_t))
# a = re.findall(my_pat,"K_xyt % (~P_xy & ~(Wxy & WumpusAlive_t))")
# for i in a:
#
#
# A = expr("OK_xyt % ~P_xy & ~(Wxy & WumpusAlive_t)")
# B = expr("~P_xy & ~(Wxy & WumpusAlive_t) &")
# m_kb = PropKB()
# m_kb.tell(A)
# m_kb.tell(B)
# C = Expr("OK_xyt")
# print(m_kb.ask(C))
# print(B)

# m_kb = PropKB()
# m_kb.tell(Expr('A'))
# a = m_kb.ask(Expr('B'))
# print(a)
# if a is False:
#     print("False")

# m_program = KB_AgentProgram(m_kb)
# m_program("Purr")

# l = []
# l.append(Expr('A'))
# l.append(Expr('D'))
# l.append(Expr('C'))
# l.append(Expr('B'))
#
# E = conj_axiom_list(l)
# print(E)

a = (1,1)
b = (1,1)
d = (1,1)
e = (1,1)
arr = []
arr.append(a)
arr.append(b)
arr.append(d)
print(arr)
x = arr.pop()
print(x)
print(arr)

# c = a is b
# print(c)
# print(a in arr)
# print(e in arr)

