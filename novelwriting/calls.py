# SPDX-FileCopyrightText: 2021 Jeff Epler
#
# SPDX-License-Identifier: GPL-3.0-only

import random
import novelwriting.driver

d = {}


def set(name, val):  #  pylint: disable=redefined-builtin
    name = name.name
    d[name] = str(val)
    return d[name]


def get(name, default=None):
    name = name.name
    if name not in d and default is not None:
        d[name] = str(default)
    return d[name]


def alternative(rule, excluded):
    e = str(excluded)
    for _ in range(100):
        s = str(rule)
        if s != e:
            break
    return s


def discard(arg):
    str(arg)
    return ""


def cap_first(rule):
    rule = str(rule)
    return rule[:1].upper() + rule[1:]


def repeat(rule, count, sep=""):
    ret = []
    for _ in range(count):
        ret.append(str(rule))
    return str(sep).join(ret)


def random_repeat(rule, min, max, sep=""):  # pylint: disable=redefined-builtin
    return repeat(rule, random.randint(min, max), sep)


def a_an(x):
    x = str(x)
    if x[0] in "aeiou":
        return "an %s" % x
    return "a %s" % x


def pluralize(x):
    x = str(x)
    if x.endswith("y"):
        return x[:-1] + "ies"
    return x + "s"


llist = {}


def laundry_list_init(ref):
    ref = ref.parts[0]
    llist[ref.name] = {}
    return ""


def laundry_list(ref, rule):
    ref = ref.parts[0]
    l = llist[ref.name]
    for _ in range(100):
        s = str(rule)
        if not s in l:
            break
    l[s] = None
    return s


def unset(s):
    s = s.name
    try:
        del d[s]
    except KeyError:
        pass
    return ""


def if_set(cond, if_true, if_false):
    if cond.name in d:
        return str(if_true)
    return str(if_false)


def if_eq(a, b, if_true, if_false):
    a = str(a)
    b = str(b)
    if a == b:
        return str(if_true)
    return str(if_false)


def expand(s):
    s = str(s)
    r = novelwriting.driver.rules[s]
    return str(r)


def possessive(s):
    s = str(s)
    if s.endswith("s"):
        return s + "'"
    return s + "'s"
