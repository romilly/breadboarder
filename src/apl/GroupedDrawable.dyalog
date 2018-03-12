:Class GroupedDrawable
    
    :Field public start 
    :Field public id
                       
    ∇ make args
    :Access Public 
    :Implements Constructor
    
     id←args
     children←⍬
     transformations←⍬
     start←0 0
    ∇

    ∇move_to xy
    :Access Public
      start←xy
      transformations,←⎕NEW #.Translation xy
    ∇

    ∇ add element
      :Access Public
      children,←element
    ∇
    
    ∇r←transformation
    :Access Public                  

    :If 0=≢transformations ⋄ r←''
    :Else ⋄ r←¯1↓1↓⍕transformations.text
    :EndIf
    ∇

    ∇ r←container
      :Access Public Overridable 
      r←⎕NEW #.Element ('g' ('id' id),(×≢transformations)/⊂'transform' transformation)
    ∇  

   
    ∇ elm←element
      :Access Public
      elm←container
      :If 0≠≢children
          elm.append¨children.element
      :EndIf
    ∇

:EndClass
