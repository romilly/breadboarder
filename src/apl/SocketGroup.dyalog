:Class SocketGroup
                
    ∇ make args;i;j;sock;label;temp
    ⍝  def __init__(self, center, rows, cols, alpha_labels, host, start_number=1, id='sockets', fill='black'):

      :Access Public
      :Implements Constructor 

      children←⍬                                                                                                               
      (center rows cols alpha_labels host start_number id fill)←8↑args,(≢args)↓(0 0) 0 0 ('' '') # 1 'sockets' 'black'    
      
      ⍝  GroupedDrawable.__init__(self)
      
        socket_size ← 2.88
        
        :For i :In ¯1+⍳cols
            :For j :In ¯1+⍳rows
                sock ← (socket fill).set_center center + #.Breadboard.PITCH × i j 
                label ← ((j+1)⊃alpha_labels),⍕i + start_number
                ⍝ host.add_port ⎕NEW #.Port (host socket.center label)
                add sock
            :EndFor
        :EndFor

    ∇       
    
    ∇r←socket fill
     ⍝   def socket(self, fill):
     ⍝   rectangle = Rectangle(self.socket_size, self.socket_size, fill=fill, stroke=fill)
     ⍝   return rectangle
    
     r←⎕NEW #.Rectangle (2/¨0 socket_size)
     r.fill←'black'
    ∇
                         
    ∇ r←container
     ⍝ Going to be an override method someday
      :Access Public
      r←⎕NEW #.Element ('g' ('id' id))
    ∇  
   
    ∇ elm←element
      :Access Public
      elm←container
      :If 0≠≢children
          elm.append¨children.element
      :EndIf
    ∇
   
    ∇ add element
      :Access Public
      children,←element
    ∇

:EndClass
