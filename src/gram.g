import driver

def go(start_rule):
    import __main__
    if 'Start' in driver.rules:
        start_rule = driver.rules['Start']
    print str(start_rule)

%%
parser NovelWriting:
    option: "use-new-regexps"
    ignore: "[ \t\n\r]+"
    token Name: "[a-zA-Z_][-a-zA-Z0-9_]*"
    token String: "\"(\\.|[^\"]*)\""
    token Number: "-?[1-9][0-9]*|0"

    rule start: prods ";;"      -> << go(prods) >>
    rule prods: prod prod_tail  -> << prod >>
    rule prod_tail:             -> << [] >>
        | prod prod_tail        -> << [prod] + prod_tail >>
    rule prod: Name ":" alt ";" -> << driver.Rule(Name, alt) >>
    rule alt: seq alt_tail      -> << driver.Alternatives(*[seq] + alt_tail) >>
        rule alt_tail:          -> << [] >>
        | "[|]" seq alt_tail    -> << [seq] + alt_tail >>
    rule seq: rep seq_tail      -> << driver.Sequence(*[rep] + seq_tail) >>
    rule seq_tail:              -> << [] >>
        | rep seq_tail          -> << [rep] + seq_tail >>
    rule rep: atom rep_tail<<atom>>   -> << rep_tail >>
        | "[(]" alt "[)]" rep_tail<<alt>> -> << rep_tail >>
    rule rep_tail<<a>>:         -> << a >>
        | "[*]"                   -> << driver.Star(a) >>
        | "[+]"                   -> << driver.Plus(a) >>
        | "[?]"                   -> << driver.Alternatives("", a) >>
    rule atom: Name             -> << driver.Reference(Name) >>
        | String                -> << eval(String) >>
        | '@' dname "[(]" args "[)]" -> << driver.Call(dname, args) >>
    rule dname: Name dname_tail -> << ".".join([Name] + dname_tail) >>
    rule dname_tail:            -> << [] >>
        | "." Name dname_tail   -> << [Name] + dname_tail >>
    rule args: arg args_tail    -> << [arg] + args_tail >>
    rule args_tail:             -> << [] >>
        | "," arg args_tail     -> << [arg] + args_tail >>
    rule arg: seq               -> << seq >>
        | Number                -> << int(Number) >>
%%
# vim:sw=4:sts=4:et:
