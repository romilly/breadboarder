:Class Breadboard : GroupedDrawable

    :Include Drawables

    :Field Public Shared PITCH←0.1×90 ⍝ 0.1 inch, 90 DPI

    :Property Default Keyed port
    :Access Public

        ∇ r←Get args
          r←ports[portnames⍳⊆⊃args.Indexers]
        ∇

    :EndProperty

    ∇ make
      :Access Public
      :Implements Constructor :Base 'breadboard'
     
      set_dimensions
      portnames←ports←⍬
     
      add ⎕NEW #.Rectangle(start(width height))
      add_power_group drop_to_top_power_group'T'
      add_numeric_labels drop_to_top_numeric_labels columns'start'
      add_body_sockets(gap_from_left_to_body_sockets drop_to_top_body_sockets)'jihgf'
      add_body_sockets(gap_from_left_to_body_sockets drop_to_lower_body_sockets)'edcba'
      add_numeric_labels drop_to_lower_numeric_labels columns'end'
      add_power_group drop_to_lower_power_group'B'
    ∇

    ∇ add_port(port label)
      :Access Public
     
      portnames,←⊂label
      ports,←port
    ∇

    ∇ add_body_sockets(center alpha_labels)
      add_alpha_labels(inset_to_left_letters(center[2]+2))alpha_labels
      add ⎕NEW #.SocketGroup(center 5 columns alpha_labels ⎕THIS)
      add_alpha_labels(inset_to_right_letters(center[2]+2))alpha_labels
    ∇

    ∇ add_alpha_labels(offset_to_letters letters);i
      :For i :In ¯1+⍳≢letters
          add(⎕NEW #.Text(((i+1)⊃letters)(offset_to_letters+0,PITCH×i)'grey' 'start' 6)).rotate ¯90
      :EndFor
    ∇

    ∇ add_numeric_labels(vertical_location count anchor);horizontal;i
      :For i :In ¯1+⍳count
          horizontal←(inset-1)+PITCH×i
          add(⎕NEW #.Text((⍕i+1)(horizontal vertical_location)'grey'anchor 6)).rotate ¯90
      :EndFor
    ∇

    ∇ add_power_group(vertical_location prefix)
    ⍝    def add_power_group(self, vertical_location, prefix):
     
      EM_DASH←⎕UCS 8212 ⍝ EM_DASH = u'\u2014'
      add_power_line(vertical_location EM_DASH'blue')
      add_power_sockets((vertical_location+drop_from_line_to_power_sockets)prefix)
      add_power_line((vertical_location+gap_between_power_lines)'+' 'red')
    ∇

    ∇ add_power_sockets(top_centre prefix);group;point
     
      :For group :In ¯1+⍳power_socket_group_count ⍝ // Would be nicer with ⎕IO←0 and array orientation instead of the loop
          point←(inset+inter_power_group_spacing×group),top_centre
          add ⎕NEW #.SocketGroup(point 2 5(prefix,¨'MP')⎕THIS(5*group))
      :EndFor
    ∇

    ∇ add_power_line args;left
    ⍝ def add_power_line(self, vertical_location, text, color):
      (vertical_location text color)←3↑args,(≢args)↓(0 0)'' 'black'
      line_offset←gap_to_left_of_power_line vertical_location ⍝ Point
      add horizontal_line line_offset(width-2×line_offset[1])color
      add(⎕NEW #.Text(text(left←line_offset+offset_from_line_start_to_text)color'middle' 7)).rotate 90
      add(⎕NEW #.Text(text(left+(width-8)¯1)color'middle' 7)).rotate 90
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

:EndClass
