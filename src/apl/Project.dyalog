:Class Project

    ∇ make
      :Access Public
      :Implements Constructor
      children←⍬
      start←0 0
    ∇
                                 
    ∇ r←container
     ⍝ Going to be an override method someday
      :Access Public
      r←⎕NEW #.Element((⊂'svg'),↓'height' 'width',⍪'480' '640')
    ∇
    
    ∇ r←Add element
      :Access Public
      children,←element
    ∇

    ∇ elm←element
      :Access Public
      elm←container
      :If 0≠≢children
          elm.append¨children.element
      :EndIf
    ∇   
    
    ∇ r←svg
      :Access Public
      r←element.Render
    ∇

:EndClass
