 r←TestDrawBreadboard;project;breadboard;svg;xml;sortstyles;pyxml;fixtrailingzeros;ports

 sortstyles←{
     0=≢styles←⍸';'∊¨⍵[;2]:⍵ ⍝ no styles
     w←⍵
     w[styles;2]←{1↓∊';',¨{⍵[⍋⍵]}((~m)×1++\m←⍵=';')⊆⍵}¨w[styles;2]
     w
 }

 fixtrailingzeros←{
     0=≢i←⍸(t←⊃¨⎕VFI¨⍵[;2])∊⊂,1:⍵
     w←⍵
     w[i;2]←⍕¨t[i]
     w
 }

 project←⎕NEW Project
 (breadboard←⎕NEW Breadboard).move_to 20 20
 project.Add breadboard
 ports←breadboard['g1' 'TP1']
 ∘∘∘
 project.Add ⎕NEW #.Wire((⊂'red'),breadboard['g1' 'TP1'])

 svg←project.svg
 xml←⎕XML svg
 xml[;4]←fixtrailingzeros¨sortstyles¨{⍵[⍋⍵;]}¨xml[;4]

 pyxml←⎕XML⊃⎕NGET'c:\devt\breadboarder\svg\bb-apl.svg'
 pyxml[;4]←fixtrailingzeros¨sortstyles¨pyxml[;4]

 r←{(≡/⍵),⍵}xml pyxml
