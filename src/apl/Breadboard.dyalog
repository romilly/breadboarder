:Class Breadboard
:Include Drawables

    ∇ make
      :Access Public
      :Implements Constructor
     
      _children←⍬
      Add ⎕NEW #.Rectangle((0 0)(192.2 291.7)) 
      Add horizontal_line (10 10) 20
    ∇

    ∇ r←Add element
      :Access Public
      _children,←element
    ∇

    ∇ r←element
      :Access Public
      r←⎕NEW #.Element'g'
      r.Add¨_children.element
    ∇

:EndClass
