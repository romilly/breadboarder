:Class SocketGroup : GroupedDrawable
                
    ∇ make args;i;j;sock;label;temp
    ⍝  def __init__(self, center, rows, cols, alpha_labels, host, start_number=1, id='sockets', fill='black'):

      :Access Public

      (center rows cols alpha_labels host start_number id fill)←8↑args,(≢args)↓(0 0) 0 0 ('' '') # 1 'sockets' 'black'    

      :Implements Constructor :Base id
      
      ⍝  GroupedDrawable.__init__(self)
      
        socket_size ← 2.88
        
        :For i :In ¯1+⍳cols
            :For j :In ¯1+⍳rows
                sock ← (socket fill).set_center center + #.Breadboard.PITCH × i j 
                label ← ((j+1)⊃alpha_labels),⍕i + start_number
                host.add_port (⎕NEW #.Port (host sock.center label)) label
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
                            
:EndClass
