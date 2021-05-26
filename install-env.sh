#!/bin/sh
python3 -mvenv .env
. .env/bin/activate
pip install wheel
pip install https://github.com/jepler/yapps/archive/master.tar.gz
pip install .
