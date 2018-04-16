The goal is to create a simple, intuitive DSL that allows you to describe a
breadboard-based electronics project and then *automatically*
1. draw a diagram of the project, and
2. generate step-by-step instructions in markdown ready for publication

The design is based on earlier closed-source tools of mine which worked but needed
improvement.

# Using the DSL

1. You typically start a project by creating a Project instance.
1. Then you add a Breadboard instance, and maybe other things, like an Arduino or Pi.
1. After that, you add wires and components.
1. When you've added all you need you can generate svg and (eventually)
generate markdown for the project.

## Current status

The core of the image generator is working.

I have started on the text/markdown generator and I do not anticipate any major
difficulties.

## Sample script and its output 
   
    def shrimp_kit():
        project = Project()
        breadboard = Breadboard().move_to(Point(20, 20))
        project.add(breadboard)
        cp = CP2102().rotate(-90., Point(40,400)).move_to(Point(40,400))
        project.add(Wire('green',cp['GND'],breadboard['a10']))
        project.add(Wire('red',cp['5V'],breadboard['a9']))
        project.add(Wire('yellow',cp['TXD'],breadboard['a4']))
        project.add(Wire('orange',cp['RXD'],breadboard['a5']))
        project.add(Wire('brown',cp['DTR'],breadboard['a2']))
        project.add(cp)
        project.add(atMega328(breadboard['f3']))
        project.add(Wire('red',breadboard['d9'],breadboard['g11']))
        project.add(Wire('green',breadboard['d10'],breadboard['g9']))
        project.add(Crystal('16Mz', breadboard['a11'], breadboard['b12']))
        project.add(Resistor('10k', '5%', breadboard['b3'], breadboard['b9']))
        project.add(Resistor('1k', '5%', breadboard['j9'], breadboard['j17']))
        project.add(DiskCapacitor('1N4', breadboard['c2'], breadboard['c3']))
        project.add(LED('red',breadboard['g12'],breadboard['g17']))
    return project
        
       
### Output
![Output](examples/shrimp.png)

The Shrimp kit and relatives are described at and available from
the [Shrimping.It website](http://start.shrimping.it/).