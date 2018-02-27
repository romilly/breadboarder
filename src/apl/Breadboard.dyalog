:Class Breadboard
    :Include Drawables

    ∇ make
      :Access Public
      :Implements Constructor
      
      start←0 0
      set_dimensions
      children←⍬      
      transformations←⍬

      Add ⎕NEW #.Rectangle(start (height width))
     ⍝ Add horizontal_line (10 10) 20
    ∇

    ∇ set_dimensions
      width←291.7
      height←192.2
      inset←19.08
      columns←30
      power_socket_group_count←5
      gap_from_left_to_body_sockets←15.2
      drop_to_top_numeric_labels←90×0.469
      drop_to_top_body_sockets←47.4
      drop_to_lower_body_sockets←108
      drop_to_lower_numeric_labels←90×1.66
      drop_to_top_power_group←5
      drop_to_lower_power_group←1.81×90
      drop_from_line_to_power_sockets←8.06
      gap_between_power_lines←24.4
      gap_to_left_of_power_line←10
      offset_from_line_start_to_text←¯8 1 ⍝ Point
      inset_to_left_letters←8
      inset_to_right_letters←90×3.18
      inter_power_group_spacing←53.5
    ∇
    
    ∇move_to xy
    :Access Public
      start←xy
      transformations,←⎕NEW #.Translation xy
    ∇

    ∇ r←Add element
      :Access Public
      children,←element
    ∇
    
    ∇r←transformation
    :Access Public
     r←¯1↓1↓⍕transformations.text
    ∇

    ∇ r←container
     ⍝ Going to be an override method someday
      :Access Public
      r←⎕NEW #.Element ('g' ('id' 'breadboard')('transform' transformation))
    ∇  
   
    ∇ elm←element
      :Access Public
      elm←container
      :If 0≠≢children
          elm.append¨children.element
      :EndIf
    ∇

:EndClass
