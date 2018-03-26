:Class Translation

    ∇ make xy
      :Access Public
      :Implements Constructor
     
      vector←xy
    ∇

    ∇ r←text
      ⍝ will override someday
      :Access Public
      r←'translate(',('¯'⎕R '-')∊(1↓¨6⍕¨vector),¨',)'
    ∇

:EndClass
