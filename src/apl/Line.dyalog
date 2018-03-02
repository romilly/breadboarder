:Class Line

    :Field Public start
    :Field Public end
    :Field Public color

    ∇ make args
⍝    def __init__(self, start, end, color='black', stroke_width=1, linecap='butt', **attributes):
      :Access Public
      :Implements Constructor
     
      (start end color)←3↑args,(≢args)↓args,0 0 'black'
    ∇

    ∇ rect←element;props
      :Access Public  
     
      props←↓'y1' 'x1' 'y2' 'x2',⍪start,end
      props,←⊂'style' ('stroke-width:1;stroke-linecap:butt;stroke:',color)
      rect←⎕NEW #.Element((⊂'line'),props)
    ∇

:EndClass
