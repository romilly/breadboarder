:Class Line

    :Field Public start
    :Field Public end

    ∇ make(s e)
⍝    def __init__(self, start, end, color='black', stroke_width=1, linecap='butt', **attributes):
      :Access Public
      :Implements Constructor
     
      (start end)←s e
    ∇

    ∇ rect←element;props
      :Access Public  
     
      props←↓'y1' 'x1' 'y2' 'x2',⍪start,end
      props,←⊂'style' 'stroke-width:1;stroke-linecap:butt;stroke:blue'
      rect←⎕NEW #.Element((⊂'line'),props)
    ∇

:EndClass
