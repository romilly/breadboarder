 r←TestDrawBreadboard;project;breadboard;svg;xml
 project←⎕NEW Project
 (breadboard←⎕NEW Breadboard).move_to 20 20
 project.Add breadboard
 svg←project.svg
 xml←⎕XML svg
 xml[;4]←{⍵[⍋⍵;]}¨xml[;4]
 r←{(≢/⍵),⍵}xml (⎕XML⊃⎕NGET'c:\devt\breadboarder\svg\bb-apl.svg')
