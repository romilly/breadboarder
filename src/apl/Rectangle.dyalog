:Class Rectangle

    :Field Public topleft
    :Field Public extent

    ∇ make(tl ex)
⍝    def __init__(self, width, height, stroke_width=1, stroke='black',rounded=False, **attributes):

      :Access Public
      :Implements Constructor
     
      (topleft extent)←tl ex
    ∇

    ∇ rect←element;props
      :Access Public  
     
      props←(↓'xy',⍪topleft),(↓'width' 'height',⍪extent)
      props,←('style' 'stroke-width:1;stroke:black')('fill' 'white')
      rect←⎕NEW #.Element((⊂'rect'),props)
    ∇

:EndClass
