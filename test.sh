#!/bin/bash

# test.sh
rm -f data/test.db
python3 -m unittest discover -s tests
