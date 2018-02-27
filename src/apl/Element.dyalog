:Class Element

    NL←⎕UCS 13

    ∇ make args;in
      :Access Public 
      :Implements Constructor
     
      tag←⊃in←,⊆args         
      props←0 2⍴⊂''
      children←⍬

      :If 0<≢in←1↓in
          'name/value pairs must have 2 elements'⎕SIGNAL(2∧.≠≢¨in)/11
          props←↑in
          'invalid names'⎕SIGNAL(80≠⎕DR¨props[;1])/11
      :EndIf
    ∇
    
    ∇ r←append element 
      :Access Public
      children,←element
    ∇

    ∇ r←Render
      :Access Public
      r←'<',tag,formatProps,'>',NL
      :If 0≠≢children
          r,←∊children.Render
      :EndIf
      r,←'</',tag,'>',NL
    ∇
    
    ∇ r←formatProps
      r←∊{' ',⍺,'="',(⍕⍵),'"'}/props
    ∇
   
    ∇ Test;s;data;z
      :Access Shared Public  

      z←(⎕NEW Element 'blah').Render    
      1=⍴('<blah>.*</blah>'⎕S'&')z~NL      
      s←⎕NEW Element ('g' ('id' 'sockets')('x' 42))
      (⎕XML'<g id="sockets" x="42" />')≡⎕XML s.Render

      s.Add ⎕NEW Element ('child' ('id' 'c1')('abc' 1)('def' 2) )
      data←⎕XML s.Render  
    ∇

:EndClass
