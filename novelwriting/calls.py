import random, novelwriting.driver

d = {}
def set(name, val):
    name = name.parts[0].name
    d[name] = str(val)
    return d[name]

def get(name, default=None):
    name = name.parts[0].name
    if not d.has_key(name) and default is not None:
        d[name] = str(default)
    return d[name]

def alternative(rule, excluded):
    e = str(excluded)
    for i in range(100):
        s = str(rule)
        if s != e: return s

def discard(arg):
    str(arg)
    return ""

def cap_first(rule):
    rule = str(rule)
    return rule[:1].upper() + rule[1:]

def repeat(rule, count, sep=""):
    ret = []
    for i in range(count):
        ret.append(str(rule))
    return str(sep).join(ret)

def random_repeat(rule, min, max, sep=""):
    return repeat(rule, random.randint(min, max), sep)

def a_an(x):
    x = str(x)
    if x[0] in "aeiou": return "an %s" % x
    return "a %s" % x

def pluralize(x):
    x = str(x)
    if x.endswith("y"): return x[:-1] + "ies"
    return x+"s"

llist = {}
def laundry_list_init(ref):
    ref = ref.parts[0]
    llist[ref.name] = {}
    return ""

def laundry_list(ref, rule):
    ref = ref.parts[0]
    l = llist[ref.name]
    for i in range(100):
        s = str(rule)
        if not s in l:
            break
    l[s] = None
    return s

def expand(s):
        s = str(s)
        r = novelwriting.driver.rules[s]
        return str(r)

