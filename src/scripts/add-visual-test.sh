#! /usr/bin/env bash
# to add a test called foo
# create a function foo in src/python/breadbaorder/examples
# invoke add-visual-test foo <description of foo> from the scripts directory
# the script will add files for appraise test, and add a call to foo in to generate
# generate an svg file
# call appraise run (which will fail on the new example)
# and copy the result file png to the examples directory
cp ../templates/test.md ../../examples/$1.md
sed -i "s/foo/$1/g;s/description/$2/" ../../examples/$1.md
echo "write_svg($1(), '$1.svg')" >> ../python/generate-test-svg.py
cd ../python
./generate-test-svg.py
cd ../..
appraise run
cp results/$1/0-actual.png examples/$1.png


