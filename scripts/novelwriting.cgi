#!/usr/bin/env python2.2

SCRIPT_DIR="/home/jepler/public_html/novelwriting-scripts"

import sys, cgi, cgitb, random, os, time
import novelwriting.gram as gram
import novelwriting.driver as driver

cgitb.enable()

fs = cgi.FieldStorage()
f0 = fn = fs['s'].value
if os.path.split(fn)[0]:
    raise RuntimeError, fn
fn = os.path.join(SCRIPT_DIR, fn)
try:
    seed = long(fs['r'].value)
except KeyError:
    seed = long(time.time()*256+os.getpid())
random.seed(seed)

def get_seed(): return str(seed)
def link_me(body, seed=seed):
    return ('<A HREF="%s?s=%s&r=%s">' % (os.environ['SCRIPT_NAME'], f0, seed) +
	str(body) +
	"</A>")

def set_header(h, v): sys.stdout.write("%s: %s\r\n" % (h, v))
content_type_set = 0
def set_content_type(t):
    global content_type_set
    content_type_set = 1
    set_header("content-type", t)

f = open(fn)
prog = f.read()
f.close()
parts = prog.split("\n;;")

if len(parts) > 1:
    code = "\n" * parts[0].count("\n") + "\n" + parts[1]
    exec code

gram.parse("included", parts[0] + ";;\n")
out = (str(driver.rules['Start']))
if not content_type_set:
    set_content_type("text/html")
set_header("content-length", len(out))
sys.stdout.write("\r\n")
sys.stdout.write(out)

# vim:sts=4:sw=4:
