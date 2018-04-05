 r←TestDrawBreadboard0;project;breadboard;svg;xml;sortstyles;pyxml;fixtrailingzeros;ports;pysvg;ToUTF8

 sortstyles←{
     w←⍵[⍋⍵;]
     0=≢styles←⍸';'∊¨w[;2]:⍵ ⍝ no styles
     w[styles;2]←{1↓∊';',¨{⍵[⍋⍵]}((~m)×1++\m←⍵=';')⊆⍵}¨w[styles;2]
     w
 }

 fixtrailingzeros←{
     0=≢i←⍸(t←⊃¨⎕VFI¨⍵[;2])∊⊂,1:⍵
     w←⍵
     w[i;2]←⍕¨t[i]
     w
 }

 ToUTF8←{⎕UCS'UTF-8'⎕UCS ⍵}

 project←⎕NEW Project
 (breadboard←⎕NEW Breadboard).move_to 20 20
 project.Add breadboard
 ⍝ ports←breadboard['g1' 'TP1']
 ⍝ project.Add ⎕NEW #.Wire((⊂'red'),breadboard['g1' 'TP1'])

 svg←project.svg
 pysvg←⊃⎕NGET'c:\devt\breadboarder\svg\bb-apl.svg'

 'F1'⎕WC'Form' 'APL Produced'('Coord' 'Pixel')('Size'(260 360))('Posn'(30 0))
 'F1.HR'⎕WC'HTMLRenderer'('AsChild' 1)('Posn'(0 0))('Size'(300 400))
 F1.HR.HTML←ToUTF8 svg

 'F2'⎕WC'Form' 'Python Produced'('Coord' 'Pixel')('Size'(260 360))('Posn'(30 400))
 'F2.HR'⎕WC'HTMLRenderer'('AsChild' 1)('Posn'(0 0))('Size'(300 400))
 F2.HR.HTML←ToUTF8 pysvg
