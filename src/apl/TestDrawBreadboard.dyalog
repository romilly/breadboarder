 r←TestDrawBreadboard;project;breadboard;svg;xml;sortstyles;pyxml

 sortstyles←{
     0=≢styles←⍸';'∊¨⍵[;2]:⍵ ⍝ no styles
     w←⍵
     w[styles;2]←{1↓∊';',¨{⍵[⍋⍵]}((~m)×1++\m←⍵=';')⊆⍵}¨w[styles;2]
     w
 }

 project←⎕NEW Project
 (breadboard←⎕NEW Breadboard).move_to 20 20
 project.Add breadboard
 svg←project.svg
 xml←⎕XML svg
 xml[;4]←sortstyles¨{⍵[⍋⍵;]}¨xml[;4]

 pyxml←⎕XML⊃⎕NGET'c:\devt\breadboarder\svg\bb-apl.svg'
 pyxml[;4]←sortstyles¨pyxml[;4]

 r←{(≡/⍵),⍵}xml pyxml
