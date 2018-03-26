:Class Text

    :Field Public text
    :Field Public start
    :Field Public color
    :Field Public anchor
    :Field Public size
    :Field Public angle←0

    ∇ make args
⍝    def __init__(self, test, start, color='black', anchore='middle', size=8, **attributes):
      :Access Public
      :Implements Constructor
      (text start color anchor size)←5↑args,(≢args)↓args,''(0 0)'black' 'middle' 8
    ∇

    ∇ r←element;props
      :Access Public
     
      props←↓'x' 'y',⍪start
      props,←⊂'style' ('fill:',color,';font-size: ',(⍕size),'pt;text-anchor:',anchor)
      
      :If angle≠0
          props,←⊂('¯'⎕R '-') 'transform' ('rotate(',(⍕angle),(∊',',¨⍕¨⌊start),')')
      :EndIf

                 
      r←⎕NEW #.Element((⊂'text'),props)
      r.text←text
    ∇

    ∇ r←rotate newangle
      :Access Public
      angle←newangle   
      r←⎕THIS
    ∇

:EndClass
