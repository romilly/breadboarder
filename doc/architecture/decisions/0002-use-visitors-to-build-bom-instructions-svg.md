# 2. Use visitors to build documentation

Date: 2018-04-17

## Status

Accepted

## Context

The Bill of Materials, Instructions and SVG are all created by visiting the
children of a project in sequence.

## Decision

The creators will all be implemented as ProjectVisitors.
A ProjectVisitor visits the project and then visits each component of the project in turn.

## Consequences

Pro:

1. Common code will be factored out
1. Project will be less cluttered
1. It will be simple to create variants of the documentation generators
and to add new generators if needed.

Con:

1. Design patterns make some developers anxious
