Add appraise test covering Shrimped breadboard with CP2102 connected.
Introduce Host, Component

(Host has ports and can be placed in a location at an angle.
It owns a GroupedDrawable.
Component is connected to ports.
Some things can be both - CP2102 for example.)

Document the svg vs. affine transformation issue.
Add unique IDs to components, sockets for use in SVG and BOM
Move Array, array_test, AFFINE.md to somewhere else as they are no londer used