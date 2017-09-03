The goal is to create a simple, intuitive DSL that allows you to describe a
breadboard-based electronics project and then *automatically*
1. draw a diagram of the project, and
2. generate step-by-step instructions in markdown ready for publication

The design is based on earlier closed-source tools which worked but needed
improvement.

# Using the DSL

1. You typically start a project by creating a Drawing instance.
1. Then you add a Breadboard instance, and maybe other things, like an Arduino or Pi.
1. After that, you add wires and components.
1. When you've added all you need you can generate svg and (eventually)
generate markdown for the project.

## Current status

The core of the image generator is working but there's work to do adding
components like capacitors, diodes and crystals.

I have not started on the text/markdown generator yet  but I do not anticipate any major
difficulties.

## Sample script and its output

    
    def test_dil():
        drawing = Drawing()
        breadboard = Breadboard()
        drawing.add(breadboard)
        breadboard.connect(atMega328(), 'f10')
        breadboard.connect(pcf8574(), 'f1')
        breadboard.connect(Wire('red'),'g1','TP1')
        breadboard.connect(Wire('black'),'a8','BM6')
        breadboard.connect(Wire('blue'),'g3','g10')
        breadboard.connect(Wire('green'),'h2','h11')
        breadboard.connect(Wire('lightgrey'),'d1','BM1')
        breadboard.connect(Wire('lightgrey'),'d2','BM2')
        breadboard.connect(Wire('lightgrey'),'d3','BM3')
        breadboard.connect(Button(), 'd8')
        breadboard.connect(Resistor('330k'), 'g17','g22')
        breadboard.connect(Resistor('2R7'), 'g25','a25')
        breadboard.connect(Resistor('1M2'), 'g27','a30')
        svg = drawing.svg()
        write(svg, 'svg/dil.svg')
        
       
### Output
![Output](docs/images/dil.png)