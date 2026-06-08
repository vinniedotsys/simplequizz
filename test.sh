#!/bin/bash

# test.sh
python3 -m unittest discover -s tests
rm -f data/test.db
