#!/bin/sh

python-lambda-local -f lambda_handler lambda_function.py event.json -t 0
