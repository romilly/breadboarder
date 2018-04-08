# 2D Affine transformations
## Theory

Affine transformations like translation, rotation, scale and shear can be implemented elegantly
using homogeneous coordinates and matrix multiplication.

There are good wikipedia articles on [Homogeneous coordinates](https://en.wikipedia.org/wiki/Homogeneous_coordinates)
and [Transformation Matrices](https://en.wikipedia.org/wiki/Transformation_matrix).

#### Homogeneous coordinates

In the 2D case, the point (x,y) can be represented as a vector (x, y ,1).

NB: If m is any non-zero value, the vector
`(mx, my, m)` represents the same point.

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

Scale and shear are not yet needed in breadboarder but their implementation is simple.

### Scale

## Transformations in APL

In APL you can generate a translation matrix using
```
     translate←{(I 3)+3 ¯3↑3 1⍴3↑⍵} where
     I←{i∘.=i←⍳⍵} generates an identity matrix.

⍝ define dot to be inner product
     dot ← +.×

⍝ Generate a translation by (5,3):

     translate 5 3
1 0 5
0 1 3
0 0 1
     T ← translate 2 ¯1 ⍝ translate by (2.-1)
      T 
1 0  2
0 1 ¯1
0 0  1   
     T dot 5 6 1
7 5 1
```

Each point can be represented in APL as a (1-d) 3-element vector or a 3×1 matrix;
multiple points can be transformed if they are represented in homogeneous coordinates as the columns of a 3×n matrix.

The trivial function `to_h` converts an array of points into homogeneous coordinates:

```
    to_h←{⍵⍪1}
    to_h 2 3
2 3 1

⍝ create a 2 × 4 matrix of four points in catestian coordinates
      points ← ?2 4⍴10
      points
7 8 3 1
1 8 5 6

⍝ convert them to homogeneous coordinates

      to_h points
7 8 3 1
1 8 5 6
1 1 1 1

⍝ translate them by (2,¯1)
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

`breadboarder.transformations.arrays` contains a (currently incomplete) implementation of an Array class,
modelled on APL arrays.

The implementation is designed for simplicity rather than performance and it contains only those features required by
*breadboarder*.


