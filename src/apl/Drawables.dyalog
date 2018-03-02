:Namespace Drawables
 
    ∇ r←horizontal_line args;start;length;color
     (start length color)←3↑args,(≢args)↓0 0 'black'
      r←⎕NEW #.Line (start(start+0 length)color)
    ∇

:EndNamespace

