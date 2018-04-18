# 3. SVGBuilder and InsructionBuilder create text but do not write it to file

Date: 2018-04-17

## Status

Accepted

## Context

The builders have enough information to create markdown and svg.

## Decision

The builders will generate text for the markdown and svg but will not
write it to file.

## Consequences

The generated output can be tested without actually writing files. 
Image entries in the markdown can use relative file locations.

