from parsers import *

s = """E
+ * id ( ) 
E E' T T' F
E -> T E'
E' -> + T E' | _                 
T -> F T'
T' -> * F T' | _
F -> id | ( E ) """
G = Grammar.read(s)
P = LL1_Parser(G)
T = P.generate()
col = []
for j in G.T + ["$"]:
    if j != G.epsilon:
        col.append(j)
print_Table(T, G.V, col)
action = []
try:
    P.parse(["id", "+", "id", "*", "id", "$"], action)
    print(action)
except ParsingError:
    print(action)
    print("Parsing Error")
except AmbigousGrammarException:
    print(action)
    print("Ambigous grammar Error")


s1 = """E
+ * ( ) id
E T F
E -> E + T | T
T -> T * F | F
F -> ( E ) | id """
G = Grammar.read(s1)
print(G)
AugG, di, dt = LR0_item.getLR0items(G)
LR0_item.print_items(AugG, dt, di)
P = LR0_parser(G)
GT = set(G.T)
GT.remove(G.epsilon)
print_Table(P.generate(), list(di.keys()), list(GT) + ["$"] + G.V, width=8)
out = P.parse(["id", "+", "id", "*", "id", "$"])
print_Table(out, list(out.keys()), ["stack", "input", "action"], width=16)
