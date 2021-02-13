from grammar import *


""""******************* UTILITIES ******************************"""

# find first of all variable in G
def First_ALL(G):
    First_T = {}
    First_V = {}
    for i in G.V:
        First_T[i] = set()
        First_V[i] = set()
    # direct entries
    for j in G.T:
        First_T[j] = set()
        First_T[j].add(j)
    for i in G.P:
        if i.prod[0] == G.epsilon:
            First_T[i.sym].add(G.epsilon)
        elif i.prod[0] in G.T:
            First_T[i.sym].add(i.prod[0])

    # indirect entries
    def inner_FirstV(G, First_T, First_V):
        for i in G.P:
            if i.prod[0] not in G.T:
                temp = set()
                tempv = set()
                temp.update(First_T[i.prod[0]])
                if i.prod[0] in G.V:
                    tempv.add(i.prod[0])
                k = 1
                while G.epsilon in temp and k < len(i.prod):
                    if i.prod[k] in G.V:
                        tempv.add(i.prod[k])
                    temp.remove(G.epsilon)
                    temp.update(First_T[i.prod[k]])
                    k += 1

                if (not temp.issubset(First_T[i.sym])) or (not temp.issubset(First_T[i.sym])):
                    First_T[i.sym].update(temp)
                    First_V[i.sym].update(tempv)
                    inner_FirstV(G, First_T, First_V)
            else:
                First_T[i.sym].add(i.prod[0])

    inner_FirstV(G, First_T, First_V)

    return First_T


# find first of a production
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
        for j in range(len(i.prod) - 1):
            if i.prod[j] not in G.T:
                Follow_T[i.prod[j]].update(First_T[i.prod[j + 1]])
                k = j + 1
                while G.epsilon in Follow_T[i.prod[j]]:
                    if k + 1 < len(i.prod):
                        Follow_T[i.prod[j]].update(First_T[i.prod[k + 1]])
                        Follow_T[i.prod[j]].remove(G.epsilon)
                    else:
                        Follow_V[i.prod[j]].add(i.sym)
                        Follow_T[i.prod[j]].remove(G.epsilon)
                    k += 1
        if i.prod[-1] not in G.T:
            Follow_V[i.prod[-1]].add(i.sym)
    for i in G.V:
        if i in Follow_V[i]:
            Follow_V[i].remove(i)

    # indirect entries
    def inner_Follow(G, Follow_T, Follow_V):
        for i in Follow_V:
            for j in Follow_V[i]:
                if not Follow_T[j].issubset(Follow_T[i]):
                    Follow_T[i].update(Follow_T[j])
                    inner_Follow(G, Follow_T, Follow_V)

    inner_Follow(G, Follow_T, Follow_V)

    return Follow_T


def print_Table(Table, row_name, col_name, width=18, title=""):
    w = width
    r = len(row_name)
    c = len(col_name)
    print("+" + ("-" * w + "+") * (c + 1))
    print("|" + title + " " * (w - len(title)) + "|", end="")
    for i in col_name:
        print(i, end=" " * (w - len(str(i))) + "|")
    print("")
    print("+" + ("-" * w + "+") * (c + 1))
    for i in row_name:
        print("|" + str(i), end=" " * (w - len(str(i))) + "|")
        for j in col_name:
            try:
                t = Table[i][j]
            except KeyError:
                t = None
            if not t:
                t = ""
            elif type(t) == type(set()):
                m = ""
                for n in t:
                    m = m + str(n) + ","
                t = m
            print(t, end=" " * (w - len(str(t))) + "|")
        print("")
        print("+" + ("-" * w + "+") * (c + 1))


#############################################################################

class AmbigousGrammarException(Exception):
    pass


class ParsingError(Exception):
    pass


class LL1_Parser:
    def __init__(self, G):
        self.G = G
        self.T = {}

    def generate(self):
        G = self.G
        # make LL1 table
        fr = First_ALL(G)
        fl = Follow_ALL(G, fr)
        Table = {}
        for i in G.V:
            Table[i] = {}
            for j in G.T + ["$"]:
                if j != G.epsilon:
                    Table[i][j] = set()
        for i in G.P:
            x = FirstV(i.prod, G, fr)
            for j in x:
                if j != G.epsilon:
                    Table[i.sym][j].add(i)
                else:
                    for k in fl[i.sym]:
                        Table[i.sym][k].add(i)
        self.T = Table
        return self.T

    def parse(self, s, action):
        prod = [self.G.S]
        t = []
        i = 0
        while i < len(s) and prod:
            x = prod[0]
            r = self.T[x][s[i]]
            if x in self.G.V:
                if len(r) == 0:
                    raise ParsingError
                elif len(r) == 1:
                    for j in r:
                        action.append(j)
                        prod = j.prod + prod[1:]
                        while prod and prod[0] in self.G.T:
                            if s[i] == prod[0]:
                                prod = prod[1:]
                                i += 1
                            elif prod[0] in self.G.epsilon:
                                prod = prod[1:]
                            else:
                                raise ParsingError

                else:
                    raise AmbigousGrammarException





# LR(0)
class LR0_item:
    def __init__(self, G, item=set()):
        self.G = G  # grammar
        self.item = item  # set of tuple ( rule number , dot postion)

    def __eq__(self, other):
        return self.G == other.G and self.item == other.item

    def __repr__(self):
        s = ""
        for i in range(len(self.G.P)):
            for j in self.item:
                if j[0] == i:
                    s += str(Rule(self.G.P[i].sym, self.G.P[i].prod[:j[1]] + ["."] + self.G.P[i].prod[j[1]:])) + "\n"
        return s

    def getDotEndingRule(self, AugG):
        r = []
        for i in self.item:
            if i[1] == len(AugG.P[i[0]].prod):
                r.append(i[0])
        return r

    def make_closure(self, symAdot):  # make closure of item
        # symAdot : set of symbol after a dot.
        G = self.G
        item = self.item
        t = symAdot
        temp = set()  # set of symbols after a dot due to new items added after making the closure
        for i in range(len(G.P)):
            if G.P[i].sym in t:
                item.add((i, 0))
                if G.P[i].prod[0] in G.V:
                    temp.add(G.P[i].prod[0])
        if not temp.issubset(t):  # check if any new symbol is added.
            t.update(temp)
            self.make_closure(t)

    def trans(self, sym):
        G = self.G
        item = self.item
        itm = set()
        for i in item:
            if i[1] < len(G.P[i[0]].prod) and sym == G.P[i[0]].prod[i[1]]:  # check if we transition dot in this rule
                itm.add((i[0], i[1] + 1))  # move dot one place
        t = set()  # symbols after dot
        for i in itm:
            if i[1] < len(G.P[i[0]].prod) and G.P[i[0]].prod[i[1]] in G.V:
                t.add(G.P[i[0]].prod[i[1]])
        if not itm:
            return None
        I = LR0_item(G, itm)  # make item
        I.make_closure(t)  # make its closure
        return I

    @staticmethod
    def getLR0items(G):
        # make augumented grammar (add S' -> S to grammar)
        AugG = Grammar(G.S + "'", G.T, [G.S + "'"] + G.V, [Rule(G.S + "'", [G.S])] + G.P)

        # create I0 first LR(0) item
        i0 = LR0_item(AugG)
        i0.item.add((0, 0))  # add S' -> .S to item
        i0.make_closure({G.S})  # manually add S as symbol after dot.

        # perform transitions
        ditems = {"I" + str(0): i0}  # map name to item
        dtrans = {}  # table of transitions ,row is symbol,col is present state, entry is next state
        for i in AugG.V + AugG.T:
            dtrans[i] = {}
        l = 0
        st = [i0]
        st_names = ["I" + str(0)]
        while st:
            j = st.pop()
            j_name = st_names.pop()
            for i in AugG.V + AugG.T:
                k = j.trans(i)
                if k:
                    flag = False
                    for x in ditems:
                        if ditems[x] == k:
                            flag = True
                            k_name = x
                    if not flag:
                        l += 1
                        ditems["I" + str(l)] = k
                        k_name = "I" + str(l)
                        st.append(k)
                        st_names.append(k_name)
                    dtrans[i][j_name] = k_name
        return AugG, ditems, dtrans

    @staticmethod
    def print_items(G, dtrans, ditems):
        print("LR(0) items")
        for i in ditems:
            print(i)
            print(ditems[i])
            print()
        print("state transition table:")
        print_Table(dtrans, G.T + G.V, list(ditems.keys()), width=8)


class LR0_parser:
    def __init__(self, G):
        self.G = G

    def generate(self):
        AugG, ditems, dtrans = LR0_item.getLR0items(self.G)

        self.AugG = AugG
        # get follow of all symbols
        flw = Follow_ALL(AugG)
        # get dot ending productions
        rules = {}
        for i in ditems:
            r = ditems[i].getDotEndingRule(AugG)
            if len(r) == 1:
                rules[i] = (flw[AugG.P[r[0]].sym], r[0])
            elif len(r) > 1:
                raise AmbigousGrammarException

        Table = {}

        for i in ditems:
            Table[i] = {}
            for j in AugG.T:
                if j != AugG.epsilon:
                    if j not in Table[i]:
                        Table[i][j] = set()
                    if i in dtrans[j]:
                        Table[i][j].add("S" + dtrans[j][i][1:])
            for j in AugG.V:
                if j not in Table[i]:
                    Table[i][j] = set()
                if i in dtrans[j]:
                    Table[i][j].add(dtrans[j][i][1:])
            Table[i]["$"] = set()
        for i in rules:
            for j in rules[i][0]:
                Table[i][j].add("R" + str(rules[i][1]))
        self.T = Table
        return Table

    def parse(self, s, action=[]):
        out = {}
        st = ["0"]
        i = 0
        v = 0
        out[v] = {}
        out[v]["stack"] = "".join(st)
        out[v]["input"] = "".join(s[i:])
        while True:
            act = list(self.T["I" + st[-1]][s[i]])
            if len(act) == 1:
                action.append(act[0])
                out[v]["action"] = act[0]
                if act[0] == "R0":
                    out[v]["action"] = "Accept"
                    break
                v += 1
                if act[0][0] == "S":
                    st.append(s[i])
                    st.append(act[0][1:])
                    i += 1
                elif act[0][0] == "R":
                    st.pop()
                    t = self.AugG.P[int(act[0][1:])]
                    y = 0
                    while y < len(t.prod) - 1:
                        if st.pop() == t.prod[-1 - y]:
                            st.pop()
                        else:
                            raise ParsingError
                        y += 1
                    if st.pop() != t.prod[-1 - y]:
                        raise ParsingError
                    st.append(t.sym)
                    o = list(self.T["I" + st[-2]][st[-1]])
                    st.append(o[0])
                if v not in out:
                    out[v] = {}
                out[v]["stack"] = "".join(st)
                out[v]["input"] = "".join(s[i:])
            else:
                raise ParsingError
        return out


