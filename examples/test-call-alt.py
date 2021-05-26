Start: @fn("a" | "b");

;;
# Due to a parser bug, @fn(a|b) used to expand to two function arguments.
def fn(x): return "Succeeded with argument %s" % x
