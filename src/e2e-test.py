from breadboarder.drawing import Drawing, Breadboard, write


def test_breadboard():
    drawing = Drawing()
    drawing.add(Breadboard())
    svg = drawing.svg()
    write(svg, 'svg/foo.svg')

test_breadboard()
