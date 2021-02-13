def print_Table(Table, row_name, col_name, width=18, title=""):
    w = width
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
            elif isinstance(t, set):
                m = ""
                for n in t:
                    m = m + str(n) + ","
                t = m
            print(t, end=" " * (w - len(str(t))) + "|")
        print("")
        print("+" + ("-" * w + "+") * (c + 1))


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
def Follow_ALL(G, First_T=None):
    if First_T is None:
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
