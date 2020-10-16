from reggie.core import *

from breadboarder.core.breadboard import Breadboard
from breadboarder.core.cp2102 import OldCP2102
from breadboarder.core.project import Project
from svg.point import Point


def word(title):
    return '(%s|%s)%s' % (title[0].upper(), title[0].lower(),title[1:])


def point_from(location):
    x, y = map(int, location.split(','))
    return Point(x,y)

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
                +  space + word('Resistor')
                ,'resistor')
color = name(one_of('red','white','black','blue','yellow','orange','pink','grey'),'color')
wire = color + space + word('Wire')
component= one_of(name(resistor,'r'),name(wire,'w'))
location = lp + d3 + comma + d3 + rp
placer = name('Put a ', 'put') + host + name(hostname, 'hostname') + ' at '+ name(location,'location') + \
         name(optional('turned '+d3+' degrees'), 'turned')
connection = word('connect') + ' a '+ component + from_pos + to_pos
step = one_of(placer, connection)


def translate(steps):
    host_classes = {'Breadboad' : Breadboard,
                    'CP2102': OldCP2102}
    project = Project()
    hosts = {}
    for step in steps:
        if len(step.strip()) == 0:
            continue
        parsed = match(step)
        if 'put' in parsed:
            host = host_classes[parsed['host']]()
            hosts[parsed['hostname']] = host
            if 'location' in parsed:
                host.move_to(point_from(parsed['location']))
            project.add(host)



print(match(step, 'put a Breadboard at (100,200)'))
print(match(connection, 'Connect a red wire from bb a12 to bb g13'))
print(match(connection, 'Connect a 10K resistor from bb a12 to bb g13'))
