from driver import Rule, alternatives, sequence, Call, Reference
import driver

def go(prods):
    if 'Start' in driver.rules:
        start_rule = driver.rules['Start']
    else:
        start_rule = prods[0]
    print repr(start_rule)
    print str(start_rule)

def include(name):
    name = eval(name, {}, {})
    f = open(name)
    try:
        return parse("included", f.read())
    finally:
        f.close()

%%
parser NovelWriting:
    option: "use-new-regexps"
    ignore: "[ \t\n\r]+"
    ignore: "#.*"
    token Name: "[a-zA-Z_][-a-zA-Z0-9_]*"
    token String: "\"(\\\\.|[^\"\\\\])*\""
    token Number: "-?[1-9][0-9]*|0"

    rule start: prods ";;"      -> << go(prods) >>
    rule included: prods ";;"   -> << prods >>
    rule prods: prod prod_tail  -> << prod + prod_tail >>
    rule prod_tail:             -> << [] >>
        | prod prod_tail        -> << prod + prod_tail >>
    rule prod: Name opt_params ":" alt ";" -> << [Rule(Name, alt, opt_params)] >>
        | "include" String      -> << include(String) >>
    rule alt: seq alt_tail      -> << alternatives(*[seq] + alt_tail) >>
        rule alt_tail:          -> << [] >>
        | "[|]" seq alt_tail    -> << [seq] + alt_tail >>
    rule seq: rep seq_tail      -> << sequence(*[rep] + seq_tail) >>
    rule seq_tail:              -> << [] >>
        | rep seq_tail          -> << [rep] + seq_tail >>
    rule rep: atom rep_tail<<atom>>   -> << rep_tail >>
        | "\[" alt "\]" rep_tail<<alt>> -> << rep_tail >>
    rule rep_tail<<a>>:         -> << a >>
        | "[*]"                 -> << driver.Star(a) >>
        | "[+]"                 -> << driver.Plus(a) >>
        | "[?]"                 -> << alternatives("", a) >>
    rule atom: Name opt_args    -> << Reference(Name, opt_args) >>
        | String                -> << eval(String, {}, {}) >>
        | '@' dname "[(]" args "[)]" -> << Call(dname, args) >>
    rule dname: Name dname_tail -> << ".".join([Name] + dname_tail) >>
    rule dname_tail:            -> << [] >>
        | "." Name dname_tail   -> << [Name] + dname_tail >>
    rule args:                  -> << [] >>
        | arg args_tail         -> << [arg] + args_tail >>
    rule args_tail:             -> << [] >>
        | "," arg args_tail     -> << [arg] + args_tail >>
    rule arg: alt               -> << alt >>
        | Number                -> << int(Number) >>
    rule opt_args:              -> << [] >>
        | "[(]" args "[)]"      -> << args >>
    rule opt_params:            -> << [] >>
        | "[(]" params "[)]"    -> << params >>
    rule params:                -> << [] >>
        | Name params_tail      -> << [Name] + params_tail >>
    rule params_tail:           -> << [] >>
        | "," Name params_tail  -> << [Name] + params_tail >>
%%
# vim:sw=4:sts=4:et:
