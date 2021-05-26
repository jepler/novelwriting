# SPDX-FileCopyrightText: 2021 Jeff Epler
#
# SPDX-License-Identifier: GPL-3.0-only

import sys
from . import gram  # pylint: disable=no-name-in-module

if len(sys.argv) == 1:
    f = sys.stdin
else:
    f = open(sys.argv[1])

prog = f.read()
parts = prog.split("\n;;\n")

if len(parts) > 1:
    exec(parts[1])  # pylint: disable=exec-used
gram.parse("start", parts[0] + ";;\n")

f.close()
