#!/bin/bash
#application will end immediately if any commands fail
set -e
echo "Running the parser"
python parser.py

echo "sleeping for 5 seconds" 
sleep 5

echo "Running the tests"
pytest -rA

echo "All tests passed now application will end"