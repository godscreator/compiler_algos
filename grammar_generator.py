class Grammar:
    def __init__(self, S, T, V, P, epsilon="_"):
        self.S = S
        self.T = T + [epsilon]
        self.V = V
        self.P = P
        self.epsilon = epsilon


# input grammar
def inputG():
    # get terminals
    T = input("Enter terminals seperated by space:").split()
    # get variables
    V = input("Enter variables seperated by space:").split()
    # get rules
    print("Enter rules of form A -> X Y | R... :")
    P = []
    while True:
        p = input(">")
        if p == "":
            break
        p = p.split("->")
        p[1] = p[1].split("|")
        for j in p[1]:
            P.append([p[0].strip(), [i.strip() for i in j.split()]])
    # get start symbol
    S = input("Enter start symbol :").strip()
    return Grammar(S, T, V, P)


def print_tab(T, name=""):
    print("\t", name)
    for j in T:
        print(j, "\t", T[j])


def print_rules(R):
    print("P:")
    for j in R:
        print(j[0], " -> ", ' '.join(j[1]))


def readG(s):
    i = s.splitlines()
    S = i[0].strip()
    T = i[1].split()
    V = i[2].split()
    P = []
    pt = i[3:]
    for j in pt:
        p = j.split("->")
        p[1] = p[1].split("|")
        for j in p[1]:
            P.append([p[0].strip(), [i.strip() for i in j.split()]])
    return Grammar(S, T, V, P)


# first of one symbol
def First(c, G, First_T, First_V):
    for i in G.P:
        if i[0] == c:
            j = 0
            while j < len(i[1]):
                # print(i,"j=",j)
                if i[1][j] in G.T:
                    First_T[i[0]].add(i[1][j])
                    break
                elif i[1][j] in G.V:
                    First(i[1][j], G, First_T, First_V)
                    # print("First_T[",i[0],"]=",First_T[i[0]])
                    First_T[i[0]].update(First_T[i[1][j]])
                    # print("First_T[",i[0],"]=",First_T[i[0]])
                    # print("First_V[",i[0],"]=",First_V[i[0]])
                    First_V[i[0]].update(First_V[i[1][j]])
                    # print("First_V[",i[0],"]=",First_V[i[0]])
                    if G.epsilon in First_T[i[1][j]]:
                        j += 1
                    else:
                        break


def FirstV(c, G, First_T):
    ans = set()
    j = 0
    ans.update(First_T[c[j]])
    k = j + 1
    while G.epsilon in ans and k < len(c):
        ans.discard(G.epsilon)
        ans.update(First_T[c[k]])
        k += 1

    return ans


def outer_First(G, First_T, First_V):
    for i in First_V:
        for j in First_V[i]:
            if not First_T[j].issubset(First_T[i]):
                First_T[i].update(First_T[j])
                outer_First(G, First_T, First_V)


def outer_FirstV(G, First_T, First_V):
    for i in G.P:
        # print("P:",i)
        if i[1][0] not in G.T:
            temp = set()
            tempv = set()
            temp.update(First_T[i[1][0]])
            if i[1][0] in G.V:
                tempv.add(i[1][0])
            k = 1
            while G.epsilon in temp and k < len(i[1]):
                if i[1][k] in G.V:
                    tempv.add(i[1][k])
                temp.remove(G.epsilon)
                temp.update(First_T[i[1][k]])
                k += 1

            if (not temp.issubset(First_T[i[0]])) or (not temp.issubset(First_T[i[0]])):
                First_T[i[0]].update(temp)
                First_V[i[0]].update(tempv)
                outer_FirstV(G, First_T, First_V)
        else:
            First_T[i[0]].add(i[1][0])


# find first of all variable in G
def First_ALL(G):
    First_T = {}
    First_V = {}
    for i in G.V:
        First_T[i] = set()
        First_V[i] = set()

    for j in G.T:
        First_T[j] = set()
        First_T[j].add(j)
    for i in G.P:
        if i[1][0] == G.epsilon:
            First_T[i[0]].add(G.epsilon)
        elif i[1][0] in G.T:
            First_T[i[0]].add(i[1][0])

    # First(G.S,G,First_T,First_V)
    # direct entries
    outer_FirstV(G, First_T, First_V)
    # print_tab(First_V,"first v")

    return First_T


def outer_Follow(G, Follow_T, Follow_V):
    for i in Follow_V:
        for j in Follow_V[i]:
            if not Follow_T[j].issubset(Follow_T[i]):
                Follow_T[i].update(Follow_T[j])
                outer_Follow(G, Follow_T, Follow_V)


# find follow of all variable in G
def Follow_ALL(G, First_T={}):
    if not First_T:
        First_T = First_ALL(G)
    Follow_T = {}
    Follow_V = {}
    for i in G.V:
        Follow_T[i] = set()
        Follow_V[i] = set()
    Follow_T[G.S].add("$")
    # direct entries
    for i in G.P:
        for j in range(len(i[1]) - 1):
            if i[1][j] not in G.T:
                Follow_T[i[1][j]].update(First_T[i[1][j + 1]])
                k = j + 1
                while G.epsilon in Follow_T[i[1][j]]:
                    if k + 1 < len(i[1]):
                        Follow_T[i[1][j]].update(First_T[i[1][k + 1]])
                        Follow_T[i[1][j]].remove(G.epsilon)
                    else:
                        # print("old Follow_V[",i[1][j],"]=",Follow_V[i[1][j]])
                        Follow_V[i[1][j]].add(i[0])
                        # print("new Follow_V[",i[1][j],"]=",Follow_V[i[1][j]])
                        Follow_T[i[1][j]].remove(G.epsilon)
                    k += 1
        if i[1][len(i[1]) - 1] not in G.T:
            Follow_V[i[1][len(i[1]) - 1]].add(i[0])
    for i in G.V:
        if i in Follow_V[i]:
            Follow_V[i].remove(i)

    outer_Follow(G, Follow_T, Follow_V)

    return Follow_T


def print_T(Table, w=18):
    g = len(G.T) + 1
    print(("-" * w + "+") * g)
    print(" " * w + "|", end="")
    for i in G.T + ["$"]:
        if i != G.epsilon:
            print(i, end=" " * (w - len(i)) + "|")
    print("")
    print(("-" * w + "+") * g)
    for i in Table:
        print(i, end=" " * (w - len(i)) + "|")
        for j in Table[i]:
            t = Table[i][j]
            if not t:
                t = ""
            else:
                m = ""
                for n in t:
                    m = m + n + ","
                t = m
            print(t, end=" " * (w - len(str(t))) + "|")
        print("")
        print(("-" * w + "+") * g)


def make_LL1(G):
    fr = First_ALL(G)
    fl = Follow_ALL(G, fr)
    Table = {}
    for i in G.V:
        Table[i] = {}
        for j in G.T + ["$"]:
            if j != G.epsilon:
                Table[i][j] = set()
    for i in G.P:
        # print("P:",i)
        x = FirstV(i[1], G, fr)
        # print("x:",x)
        for j in x:
            if j != G.epsilon:
                Table[i[0]][j].add(i[0] + " -> " + ' '.join(i[1]))
            else:
                for k in fl[i[0]]:
                    Table[i[0]][k].add(i[0] + " -> " + ' '.join(i[1]))
    return Table


# LR(0)

def make_Aug_grammar(G):
    G.V = [G.S + "'"] + G.V
    G.P = [[G.S + "'", [G.S]]] + G.P
    G.S = G.S + "'"


def make_closure(G, item, symAdot):
    t = symAdot
    temp = set()
    for i in range(len(G.P)):
        if G.P[i][0] in t:
            item.append((i, 0))
            temp.add(G.P[i][1][0])
    if not temp.issubset(t):
        t.update(temp)
        make_closure(G, item, t)


def create_item(G, prodc_n, dot_n):
    o = [(prodc_n, dot_n)]
    t = set()
    for i in o:
        # print("i[0]",i[0])
        # print("G.P[i[0]]",G.P[i[0]])
        if i[1] < len(G.P[i[0]][1]):
            t.add(G.P[i[0]][1][i[1]])
    # print(o)
    make_closure(G, o, t)

    return tuple(set(o))


def trans(G, item, sym):
    itm = []
    for i in item:
        # print("i[0]",i[0])
        # print("G.P[i[0]]",G.P[i[0]])
        if i[1] < len(G.P[i[0]][1]) and sym == G.P[i[0]][1][i[1]]:
            itm.append((i[0], i[1] + 1))
    t = set()
    for i in itm:
        if i[1] < len(G.P[i[0]][1]):
            t.add(G.P[i[0]][1][i[1]])
    make_closure(G, itm, t)
    return tuple(set(itm))


def getLR0items(G):
    make_Aug_grammar(G)
    i0 = create_item(G, 0, 0)
    ditems = {}
    ditems[i0] = "I" + str(0)
    dtrans = {}
    for i in G.V + G.T:
        dtrans[i] = {}
    l = 0
    st = [i0]
    while st:
        j = st.pop()
        for i in G.V + G.T:
            k = trans(G, j, i)
            if k:
                if k not in ditems:
                    l += 1
                    ditems[k] = "I" + str(l)
                    st.append(k)
                dtrans[i][ditems[j]] = ditems[k]
    dnames = {}
    for i in ditems:
        dnames[ditems[i]] = i
    return ditems, dtrans, dnames


def print_item(G, item):
    t = []
    ##    for i in item:
    ##        #print("i[0]",i[0])
    ##        s = G.P[i[0]][0]
    ##        r = G.P[i[0]][1][:i[1]]+["."]+G.P[i[0]][1][i[1]:]
    ##        t.append([s,r])
    for j in range(len(G.P)):
        for i in item:
            if i[0] == j:
                # print("i[0]",i[0])
                s = G.P[i[0]][0]
                r = G.P[i[0]][1][:i[1]] + ["."] + G.P[i[0]][1][i[1]:]
                t.append([s, r])
    print_rules(t)


def print_items(G, dtrans, ditems, dnames):
    for i in dnames:
        print(i)
        print_item(G, dnames[i])
    for k in range(len(dnames)):
        for i in dtrans:
            for j in dtrans[i]:
                if j == "I" + str(k):
                    print("(", j, ",", i, ")=", dtrans[i][j])
                    # print_item(G,dnames[dtrans[i][j]])


##s1 = """E
##+ * ( ) id
##E E' T T' F
##E -> T E'
##E' -> + T E' | _
##T -> F T'
##T' -> * F T' | _
##F -> ( E ) | id"""
s = """ S
a b
S P
S -> P P
P -> a P | b
"""
G = readG(s)
print_rules(G.P)
fr = First_ALL(G)
print_tab(fr, "First")
fl = Follow_ALL(G, fr)
print_tab(fl, "Follow T")
T = make_LL1(G)
print_T(T)
##s1 = """S
##+ a b c
##S A B
##S -> S + A
##A -> B
##B -> a | b | c """
##G = readG(s1)
##print_rules(G.P)
##di,dt,dn = getLR0items(G)
##print_items(G,dt,di,dn)
