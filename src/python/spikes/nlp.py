from reggie.core import *

def w(title):
    return '(%s|%s)%s' % (title[0].upper(), title[0].lower(),title[1:])

d = '\d'
od = '\d?'
d3 = multiple(digit, 1, 3)
resistance = one_of(d+'R'+od, d3+'R',d+'K'+od, d3+'K', d+'M'+od, d3+'M')
tolerance = one_of('1','5','10')+'%'
host = name(one_of('Breadboard','CP2102'),'host')
hostname = letter + multiple(an)
port = multiple(letter) + multiple(d, 0, 3)
from_pos = name(' from ' + hostname + space + port, 'from')
to_pos = name(' to ' + hostname + space + port,'to')
resistor = name(name(resistance,'res')
                + optional(name(tolerance,'tol'))
                +  space + w('Resistor')
                ,'resistor')
color = name(one_of('red','white','black','blue','yellow','orange','pink','grey'),'color')
wire = color + space + w('Wire')
component= one_of(name(resistor,'r'),name(wire,'w'))
location = lp+d3+comma+d3+rp
placer = w('Put a ') + host +  ' at '+ name(location,'location') + \
         name(optional('turned '+d3+' degrees'), 'turned')
connection = w('connect') + ' a '+ component + from_pos + to_pos
step = one_of(placer, connection)
print(connection)
# print(match(step, 'put a Breadboard at (100,200)'))
print(match(connection, 'Connect a red wire from bb a12 to bb g13'))
print(match(connection, 'Connect a 10K resistor from bb a12 to bb g13'))
