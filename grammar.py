class Rule:
    # sym -> prod
    def __init__(self, sym, prod):
        self.sym = sym
        self.prod = prod

    def __repr__(self):
        return self.sym + " -> " + ' '.join(self.prod)


class Grammar:
    def __init__(self, S, T, V, P, epsilon="_"):
        self.S = S
        self.T = T + [epsilon]
        self.V = V
        self.P = P
        self.epsilon = epsilon

    def __eq__(self, other):
        x = self.S == other.S
        x = x and self.T == other.T
        x = x and self.V == other.V
        x = x and self.P == other.P
        return x

    # input grammar
    @staticmethod
    def input():
        # get start symbol
        S = input("Enter start symbol :").strip()
        # get terminals
        T = input("Enter terminals seperated by space:").split()
        # get variables
        V = input("Enter variables seperated by space:").split()
        # get rules
        print("Enter rules of form A -> X1 X2 .. | Y1 Y2 .. | .. :")
        P = []
        while True:
            p = input(">")
            if p == "":
                break
            p = p.split("->")
            p[1] = p[1].split("|")
            for j in p[1]:
                P.append(Rule(p[0].strip(), [i.strip() for i in j.split()]))

        return Grammar(S, T, V, P)

    # input grammar from string
    @staticmethod
    def read(s):
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
                P.append(Rule(p[0].strip(), [i.strip() for i in j.split()]))
        return Grammar(S, T, V, P)

    # print grammar
    def print(self):
        print("G(S=", self.S, ",T=", self.T, ",V=", self.V, "P)")
        for i in self.P:
            print(i)
