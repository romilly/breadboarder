:Class Port

    ∇ make args
      :Implements Constructor
      :Access Public

      (host center label)←args
    ∇

    ∇ r←location
      :Access Public
     
      r←center+host.start
      ∇

:EndClass
