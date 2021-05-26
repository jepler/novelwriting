# SPDX-FileCopyrightText: 2021 Jeff Epler
#
# SPDX-License-Identifier: GPL-3.0-only

"""Low-level implementation details of novelwriting"""

import random


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
    def __add__(self, other):
        return Sequence(self, other)

    def __radd__(self, other):
        return Sequence(other, self)

    def __or__(self, other):
        return Alternatives(self, other)

    def __ror__(self, other):
        return Alternatives(other, self)


class Alternatives(Concatable):
    def __init__(self, *alts):
        self.alternatives, self.weight = weight(alts)

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
        raise RuntimeError("unreachable")

    def __repr__(self):
        return "<Alternatives %s>" % map(short, self.alternatives)

    @staticmethod
    def __short__():
        return "<Alternatives>"


def alternatives(*alts):
    a = weight(alts)[0]
    if len(a) == 1:
        return a[0][1]
    return Alternatives(*alts)


class Sequence(Concatable):
    def __init__(self, *parts):
        self.parts = parts

    def __str__(self):
        return "".join([str(i) for i in self.parts])

    def __add__(self, other):
        if isinstance(other, Sequence):
            return Sequence(*(self.parts + other.parts))
        return Sequence(*(self.parts + (other,)))

    def __repr__(self):
        return "<Sequence %s>" % map(short, self.parts)

    @staticmethod
    def __short__():
        return "<Sequence>"


def sequence(*parts):
    if len(parts) == 1:
        return parts[0]
    return Sequence(*parts)


rules = {}
_anon_ruleno = 0


class Reference(Concatable):
    def __init__(self, name=None, args=None):
        if args is None:
            args = []
        global _anon_ruleno  # pylint: disable=global-statement
        if name is None:
            name = _anon_ruleno
            _anon_ruleno += 1
        self.name = name
        self.args = args

    def __str__(self):
        global rules  # pylint: disable=global-statement
        rule = rules[self.name]
        if not isinstance(rule, Rule):
            if self.args:
                raise TypeError(
                    "Rule %s takes no arguments (%s given)"
                    % (self.name, len(self.args))
                )
            return str(rule)
        if len(self.args) != len(rule.args):
            raise TypeError(
                "Rule %s takes %s argument%s (%s given)"
                % (
                    rule.name,
                    len(rule.args),
                    ["", "s"][len(rule.args) != 1],
                    len(self.args),
                )
            )
        old_rules = rules.copy()
        for i, name in enumerate(rule.args):
            rules[name] = str(self.args[i])
        ret = str(rules[self.name])
        rules = old_rules
        return ret

    def __repr__(self):
        return "<Reference %s>" % self.name


class Rule(Concatable):
    def __init__(self, name, body, args=None):
        self.name = name
        self.body = body
        if args is None:
            self.args = []
        else:
            self.args = args
        rules[name] = self

    def __str__(self):
        return str(self.body)

    def __repr__(self):
        return "<Rule %s>" % self.name


def Star(body):
    r = Reference()
    return Rule(r.name, Alternatives(body, r + body))


def Plus(body):
    return Star(body) + body


class Call(Concatable):
    def __init__(self, fun_name, args):
        self.fun_name = fun_name.replace("-", "_")
        self.args = args

    def __str__(self):
        fun = getattr(__import__("__main__"), self.fun_name)
        ret = fun(*self.args)
        if ret is None:
            return ""
        return str(ret)

    def __repr__(self):
        return "<Call %s %s>" % (self.fun_name, short(self.args))

    def __short__(self):
        return "<Call %s>" % self.fun_name


class Pluralize(Concatable):
    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        return str(self.rule) + "s"

    @staticmethod
    def __short__():
        return "<Pluralize>"


def short(x):
    if hasattr(x, "__short__"):
        return x.__short__()
    return repr(x)


def main():
    C = Rule("C", Alternatives("a", "b", (0.5, "c")))
    D = Rule("D", Alternatives(C, "xx"))
    E = Rule("E", Alternatives(D, (2, Reference("E") + D)))
    F = Star("*")
    Animal = Alternatives("cat", "dog", "hyena", "tapir")
    G = "It's raining " + Pluralize(Animal) + " and " + Pluralize(Animal)
    H = "A " + Animal + " and a rabbi walk into a bar"
    Joke = G + "." | H + "." | G + ".  " + H + "." | H + ".  " + G + "."
    S = Rule("S", (E | F) + "$")
    print(rules)

    for _ in range(10):
        print(S)

    for _ in range(10):
        print(Joke)


if __name__ == "__main__":
    main()

# vim:sw=4:sts=4:et:
