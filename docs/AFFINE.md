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

Scale and shear are not yet needed in breadboarder.

## Transformations in APL

In APL you can generate a translation matrix using
```
translate←{(I 3)+3 ¯3↑3 1⍴3↑⍵} where
I←{i∘.=i←⍳⍵} generates an identity matrix.

⍝ Generate a translation by (5,3):

     translate 5 3
1 0 5
0 1 3
0 0 1
     T ← translate 2 ¯1 ⍝ translate by (2.-1)
     T+.×5 6 1
7 5 1
```
You can generate a rotation matrix using
```
rotate←{0 0 1⍪⍨2 3↑(2 2⍴1 1 ¯1 1×2 1 1 2○⍵)} ⍝ ⍵ in radians
to_radians←{⍵×○÷180} ⍝ convert degrees to radians

rotate to_radians 45
0.7071067812  0.7071067812 0
¯0.7071067812 0.7071067812 0
0             0            1

⍝ rotate the point (1,0) by -60 degrees


```

## Transformations in Python

To be added
