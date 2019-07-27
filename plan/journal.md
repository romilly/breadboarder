# Project Journal for breadboarder

## Friday 26 July 2019

I'm going to get the tests running again.

I use [*appraise*](https://github.com/AppraiseQA/appraise) for image-based testing.

I've moved all the current e2e tests to `breadboarder.examples`, 
and they are now used to create svg files.

I'll set up a Python script that runs them all: `generate_appraise_files/generate.py`

## Saturday 27 July 2019

I'll set up a bash script that

1. generates all the test svg files
1. runs appraise

and then move the *ann*-related classes into this project for drawing networks. 


