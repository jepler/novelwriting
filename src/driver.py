import random, bisect

def weight(l):
    c = 0
    r = []
    for i in l:
        if isinstance(i, tuple):
            w, p = i
        else:
            w, p = 1, i
        c = c + w
        r.append((c, p))
    return r, c


class Concatable:
    def __add__(self, other): return Sequence(self, other)
    def __radd__(self, other): return Sequence(other, self)
    def __or__(self, other): return Alternatives(self, other)
    def __ror__(self, other): return Alternatives(other, self)

class Alternatives(Concatable):
    def __init__(self, *alternatives):
        self.alternatives, self.weight = weight(alternatives)

    def addrule(self, a, b=None):
        if b is None:
            self.alternatives.append((self.weight, a))
            self.weight = self.weight + 1
        else:
            self.alternatives.append((self.weight, b))
            self.weight = self.weight + a

    def __str__(self):
        r = random.random() * self.weight
        for i, j in self.alternatives:
            if r < i:
                return str(j)


class Sequence(Concatable):
    def __init__(self, *parts):
        self.parts = parts

    def __str__(self):
        return "".join([str(i) for i in self.parts])
    def __add__(self, other):
        if isinstance(other, Sequence):
            return Sequence(*(self.parts + other.parts))
        return Sequence(*(self.parts + (other,)))

rules = {}
_anon_ruleno = 0
class Reference(Concatable):
    def __init__(self, name=None):
        global _anon_ruleno
        if name is None:
            name = _anon_ruleno
            _anon_ruleno += 1
        self.name = name
    def __str__(self):
        return str(rules[self.name])

class Rule(Concatable):
    def __init__(self, name, body):
        self.name = name
        self.body = body
        rules[name] = self

    def __str__(self):
        return str(self.body)

def Star(body):
    r = Reference()
    return Rule(r.name, Alternatives(body, r + body))

def Plus(body):
    return Star(body) + body

#def pluralize(r):
#        if r.endswith("y"): return r[:-1] + "ies"
#        return r+"s"

class Call(Concatable):
    def __init__(self, fun_name, args):
        self.fun_name = fun_name.replace("-", "_")
        self.args = args

    def __str__(self):
        fun = eval(self.fun_name, __import__("__main__").__dict__)
        return fun(*self.args)

class Pluralize(Concatable):
    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        r = str(self.rule)

if __name__ == '__main__':
    C = Rule("C", Alternatives("a", "b", (.5, "c")))
    D = Rule("D", Alternatives(C, "xx"))
    E = Rule("E", Alternatives(D, (2, Reference("E") + D)))
    F = Star("*")
    Animal = Alternatives("cat", "dog", "hyena", "tapir")
    G = "It's raining " + Pluralize(Animal) + " and " + Pluralize(Animal)
    H = "A " + Animal + " and a rabbi walk into a bar"
    Joke = G+"." | H+"." | G+".  "+H+"." | H+".  "+G+"."
    S = Rule("S", (E|F) + "$")
    print rules

    for i in range(10):
        print S

    for i in range(10):
        print Joke

# vim:sw=4:sts=4:et:
