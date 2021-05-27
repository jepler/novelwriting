# SPDX-FileCopyrightText: 2021 Jeff Epler
#
# SPDX-License-Identifier: GPL-3.0-only

%%
parser NovelWriting:
    ignore: "[ \t\n\r]+"
    ignore: "#.*"
    token Name: "[a-zA-Z_][-a-zA-Z0-9_]*"
    token String: "\"(\\\\.|[^\"\\\\])*\""
    token Number: "-?[1-9][0-9]*|0"

    rule start: prods ";;"      {{ return go(prods) }}

    rule included: prods ";;"   {{ return prods }}

    rule prods:                 {{ result = [] }}
        (prod                   {{ result.append(prod) }} )*
                                {{ return result }}

    rule prod:
        Name opt_params ":" alt ";"
                                {{ return Rule(Name, alt, opt_params) }} |
        "include" String        {{ return include(String) }}

    rule alt: seq               {{ result = [seq] }}
        ( "[|]" seq             {{ result.append(seq) }} )*
                                {{ return alternatives(*result) }}

    rule seq:                   {{ result = [] }}
        (rep                    {{ result.append(rep) }} )+
                                {{ return sequence(*result) }}

    rule rep: atom rep_tail<<atom>>   {{ return rep_tail }}
        | "\[" alt "\]" rep_tail<<alt>> {{ return rep_tail }}
    rule rep_tail<<a>>:         {{ result = a }}
        ( "[*]"                 {{ result = driver.Star(a) }}
        | "[+]"                 {{ result = driver.Plus(a) }}
        | "[?]"                 {{ result = alternatives("", a) }}
        )?
                                {{ return result }}

    rule atom: Name opt_args    {{ return Reference(Name, opt_args) }}
        | String                {{ return eval(String, {}, {}) }}
        | '@' dname opt_args    {{ return Call(dname, opt_args) }}

    rule dname: Name            {{ result = [Name] }}
        ( "[.]" Name            {{ result.append(Name) }}) *
                                {{ return ".".join(result) }}

    rule args: arg              {{ result = [arg] }}
        ( "," arg               {{ result.append(arg) }} ) *
        "," ?                   {{ return result }}

    rule arg: alt               {{ return alt }}
        | Number                {{ return int(Number) }}

    rule opt_args:              {{ result = [] }}
        (
            "[(]"
            (
                arg             {{ result.append(arg) }}
                ( "," arg       {{ result.append(arg) }} ) *
                "," ?
            )?
            "[)]"
        )?
                                {{ return result }}

    rule opt_params:            {{ result = [] }}
        ("[(]" params "[)]"     {{ result = params }} )?
                                {{ return result }}

    rule params:
        Name                    {{ result = [Name] }}
        ( ',' Name              {{ result.append(Name) }} ) *
                                {{ return result }}
%%
from .driver import Rule, alternatives, sequence, Call, Reference
from . import driver

def go(prods):
    if 'Start' in driver.rules:
        start_rule = driver.rules['Start']
    else:
        start_rule = prods[0]
    print(str(start_rule))

def include(name):
    name = eval(name, {}, {})
    f = open(name)
    try:
        return parse("included", f.read())
    finally:
        f.close()
# vim:sw=4:sts=4:et:
