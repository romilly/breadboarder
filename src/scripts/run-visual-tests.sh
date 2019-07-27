#!/usr/bin/env bash
cd $1/src/python
./generate-test-svg.py $1
cd $1
appraise run


