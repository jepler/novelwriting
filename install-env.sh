#!/bin/sh

# SPDX-FileCopyrightText: 2021 Jeff Epler
#
# SPDX-License-Identifier: GPL-3.0-only

python3 -mvenv .env
. .env/bin/activate
pip install wheel
pip install https://github.com/jepler/yapps/archive/master.tar.gz
pip install .
