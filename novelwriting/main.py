import gram, sys

if len(sys.argv) == 1:
    f = sys.stdin
else:
    f = open(sys.argv[1])

prog = f.read()
parts = prog.split("\n;;\n")

if len(parts) > 1:
    exec parts[1] 
gram.parse("start", parts[0] + ";;\n")

f.close()
