# Affine transformations in *breadboarder*

This document explains the requirement for Affine transformations in *breadboarder*.
It also documents the design decisions behind the Python implementation.

At some point the document is likely to be merged into more comprehensive documentation for *breadboarder*.

Some of the Python transformation code was prototyped in APL and there is a brief description of the APL protoype.
The APL code and its description will be removed at some point.

## Why Affine transformations?

This section describes a difficulty that arises when using *breadboarder* for all but the simplest designs,
and explains how Affine transformations resolve the problem.

### *breadboarder* components and connections

A typical *breadboarder* project consists of connected *compound components* (like a breadboard, an Arduino or a
BBC micro:bit) and *basic components* (like wires, resistors, capacitors, switches, or diodes).

Compound components have connection points (called *ports*). Basic components connect two or more ports on one or more
compound components.

When you lay out a *breadboarder* project it is convenient to be able to move and rotate compound components before you
specify their connections.

### Locating ports

Components in *breadboarder* are rendered as SVG groups. SVG provides suitable transformations
(translations and rotations) that you can use to position the components,but this raises a potential problem.

A basic component can be used to connect different compound components which will be rendered by distinct SVG groups.

The component's location in the diagram will be determined byt the position its endpoints. These are determined by the
position of the ports to which it is connected.

The ports may belong to different compound components (an Arduino and a breadboard, for example) that are rendered by
distinct SVG groups so the locations of the ports cannot be determined by SVG.

The solution is to write Python code to turn the relative locations of the ports and
their parent compound components into into absolute coordinates. Then *breadboarder* can generate SVG to draw the basic
components in their correct locations.

The process can easily be implemented using
[Affine transformations](https://en.wikipedia.org/wiki/Affine_transformation).

## Theory

Affine transformations like translation, rotation, scale and shear can be implemented elegantly
using homogeneous coordinates and matrix multiplication.

There are good wikipedia articles on [Homogeneous coordinates](https://en.wikipedia.org/wiki/Homogeneous_coordinates)
and [Transformation Matrices](https://en.wikipedia.org/wiki/Transformation_matrix).

#### Homogeneous coordinates

In the 2D case, the point (x,y) can be represented as a vector `(x, y ,1)`.

If m is any non-zero value, the vector `(mx, my, m)` represents the same point.

### Translation

If the plane is translated by (X,Y), the new coordinates of the point (x,y) can be obtained by multiplying the matrix

```
1 0 X
0 1 Y
0 0 1
```
by the vector `(x,y,1)`

to give a new vector `(x+X, y+Y, 1)`

### Rotation

If the plane is rotated about the origin by an angle θ, the new coordinates of the point (x,y) can be obtained by multiplying the matrix

```
 cos(θ) sin(θ) 0
-sin(θ) cos(θ) 0
 0      0      1
```
by the vector `(x,y,1)` to give the new location of the point in homogeneous coordinates.

Scale and shear are not needed in *breadboarder*.

The code to generate and apply Affine transofrmations was prototyped in APL before coding in Python.

## Transformations in APL

In APL you can generate a translation matrix using
```
     translate←{(I 3)+3 ¯3↑3 1⍴3↑⍵} where
     I←{i∘.=i←⍳⍵} generates an identity matrix.

⍝ define dot to be inner product
     dot ← +.×

     T ← translate 2 ¯1 ⍝ translate by (2.-1)
     T 
1 0  2
0 1 ¯1
0 0  1   
     T dot 5 6 1
7 5 1
```

Each point can be represented in APL as a (1-d) 3-element vector or a 3×1 matrix.

Multiple points can be transformed if they are represented in homogeneous coordinates as the columns of a 3×n matrix.

The trivial function `to_h` converts an array of points into homogeneous coordinates:

```
    to_h←{⍵⍪1}
    to_h 2 3
2 3 1

⍝ create a 2 × 4 matrix of four points in cartesian coordinates
      points ← ?2 4⍴10
      points
7 8 3 1
1 8 5 6

⍝ convert them to homogeneous coordinates

      to_h points
7 8 3 1
1 8 5 6
1 1 1 1

⍝ translate them by (2,¯1) using T defied above
      xp ← T dot to_h points
      xp
9 10 5 3
0  7 4 5
1  1 1 1

⍝ homogeneous coordinates can be converted back to cartesian coordinates using to_c

     to_c←{¯1↓⍵÷(¯1↑⍵)⍴⍨⍴⍵}
     to_c xp
9 10 5 3
0  7 4 5

⍝ we can multiply homogenous coordinates by any non-zero value without changing the point(s) they represent.
      to_c 2×xp
9 10 5 3
0  7 4 5

```


You can generate a rotation matrix using
```
rotate←{0 0 1⍪⍨2 3↑(2 2⍴1 1 ¯1 1×2 1 1 2○⍵)} ⍝ ⍵ in radians
to_radians←{⍵×○÷180} ⍝ convert degrees to radians

      rm60 ← rotate radians -60
      rm60
0.5          ¯0.8660254038 0
0.8660254038  0.5          0
0             0            1

⍝ rotate the point (1,0) by -60 degrees

      to_c rm60 dot to_h 1 0
0.5 0.8660254038
```

## Transformations in Python

It would be easy to implement matrix-based transformations in Python using numpy, but this would add a significant
dependency to *breadboarder*.

`breadboarder.transformations.arrays` contains a partial implementation of an Array class,
modelled on APL arrays.

The implementation is designed for simplicity rather than performance and it contains only those features required by
*breadboarder*. It does little error checking as the Arrays used in breadboarder are all of compatible shapes.

I did not implement separate classes for Vector and Matrix as I wanted to avoid duplicated code.

## The Array class

An Array is constructed from a shape and a list of elements.

The shape can be a list or a vector (a one-dimensional Array).

Inner product is implemented as a `dot` method in the Array class. It handles vector, matrix and tensor
arguments. It does not support scalar extension as this is not needed in *breadboarder*.

## Transformations and other changes

*breadboarder* already contains Transformation classes. These will be enhanced to generate their corresponding
transformation arrays.

Since basic components and compound components are treated differently, this now needs to be reflected in the
class hierarchy.

## Tests

I am writing some integration tests to verify that the port locations of compound components with
multiple transformations are correctly calculated.




