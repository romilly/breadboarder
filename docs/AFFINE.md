# 2D Affine transformations
## Theory

Affine transformations like translation, rotation, scale and shear can be implemented elegantly using homogeneous coordinates and matrix multiplication.

#### Homogeneous coordinates

In the 2D case, the point (x,y) can be represented as a vector (x, y ,1)

If m is any non-zero value, the vector
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

Scale and shear to be added.

## Transformations in APL

To be added

## Transformations in Python

To be added
