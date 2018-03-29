import abc

from breadboarder.core.breadboard import Breadboard
from breadboarder.core.svg import GroupedDrawable, Rectangle, Point, PolygonalPath, Text, Circle, Path, vector, arc


def cms(distance):
    return distance * Breadboard.PITCH / 0.254

def ins(distance):
    return distance * Breadboard.PITCH * 10


class RectangularLed(GroupedDrawable):
    def __init__(self, point):
        GroupedDrawable.__init__(self, svg_id='muled')
        self.WIDTH = cms(0.1)
        self.HEIGHT = cms(0.2)
        self.add(Rectangle(self.WIDTH, self.HEIGHT, fill='red', stroke='none').move_to(point))


class MicrobitConnector(GroupedDrawable):
    CONNECTOR_SPACING = 0.0492
    WIDTH = 0.04
    C_HEIGHT = cms(0.54)

    def __init__(self,add_text=True):
        GroupedDrawable.__init__(self, svg_id='microbit connector')
        self.wide_connector_start_positions = [1, 9, 18, 27, 35]
        self.add_end_connectors()
        self.add_wide_connectors(add_text)
        self.add_narrow_connectors()

    def wide_connector_spans(self):
        result = []
        for pos in self.wide_connector_start_positions:
            for i in range(4):
                result.append(pos+i)
        return result

    def add_end_connectors(self):
        self.add(Path(Point(4,-self.C_HEIGHT),vector(-4, 0),
                      vector(0,self.C_HEIGHT-4), arc(4,4,0,0,0,4,4), fill='gold'))
        self.add(Path(Point(cms(5.0)-4,-self.C_HEIGHT),vector(4, 0),
                      vector(0,self.C_HEIGHT-4), arc(4,4,0,0,1,-4,4), fill='gold'))

    def offset(self, index):
        return 0.5+ins(index*self.CONNECTOR_SPACING)

    def add_wide_connectors(self,add_text):
        texts = ['0','1','2','3V','GND'] if add_text else 5*['']
        specs = zip(self.wide_connector_start_positions, texts)
        for (pos, text) in specs:
            self.add(self.wide_connector(pos, text))

    def add_narrow_connectors(self):
        for i in set(range(40)) - (set([0,39]+self.wide_connector_spans())):
            self.add(Rectangle(ins(self.WIDTH),self.C_HEIGHT, fill='gold', stroke='none').move_to(Point(self.offset(i),-self.C_HEIGHT)))

    def wide_connector(self, pos, text):
        g = GroupedDrawable(text)
        g.add(Rectangle(ins(self.WIDTH+3*self.CONNECTOR_SPACING),cms(0.65), fill='gold', stroke='none')
             .move_to(Point(self.offset(pos),cms(-0.65))))
        centre = Point(ins(0.5*self.WIDTH+self.CONNECTOR_SPACING)+self.offset(pos+1)-2,cms(-0.7))
        if text:
            g.add(Text(text, Point(centre.x, cms(-0.2)),anchor='middle',size=6))
        g.add(Circle(Point(0,0),cms(0.27),fill='gold').
              move_center_to(centre))
        g.add(Circle(Point(0,0),cms(0.245),fill='white').
              move_center_to(centre))
        return g


class MicrobitButton(GroupedDrawable):
     def __init__(self):
         GroupedDrawable.__init__(self, svg_id='button')
         self.add(Rectangle(cms(0.625),cms(0.62), fill='silver', stroke='none'))
         self.add(Circle(Point(cms(0.13),cms(0.13)),cms(0.5*0.37)))


class MicroBit(GroupedDrawable):
    __metaclass__ = abc.ABCMeta

    def __init__(self, svg_id):
         GroupedDrawable.__init__(self, svg_id=svg_id)
         self.add(Rectangle(height=cms(4.2), width=cms(5.0), rounded=True, fill='grey', stroke='none'))

    @abc.abstractmethod
    def add_parts(self):
        pass


    def add_button(self, left, top):
        self.add(MicrobitButton().move_to(Point(left, top)))


class MicrobitBack(MicroBit):
    def __init__(self):
        MicroBit.__init__(self, svg_id='microbit back')
        self.add_parts()

    def add_parts(self):
        self.add_jst_power_socket()
        self.add_usb_port_back()
        self.add_button(cms(3.14),0)
        self.add(MicrobitConnector(add_text=False).move_to(Point(0, cms(4.2))))

    def add_jst_power_socket(self):
        self.add(Rectangle(height=cms(0.58), width=cms(0.8), fill='antiquewhite', stroke='none').move_to(Point(cms(5.0-(0.8+0.23)),0)))

    def add_usb_port_back(self):
        self.add(Rectangle(height=cms(0.4),width=cms(0.55),fill='silver', stroke='none').move_to(Point(cms(2.4),-cms(0.1))))

class MicrobitFront(MicroBit):
    def __init__(self):
        MicroBit.__init__(self, svg_id='microbit front')
        self.add_parts()

    def add_parts(self):
        self.add_usb_port_front()
        self.add_decoration()
        self.add_logo()
        self.add_leds()
        self.add_buttons()
        self.add_button_labels()
        self.add(MicrobitConnector().move_to(Point(0, cms(4.2))))

    def add_usb_port_front(self):
        self.add(Rectangle(height=cms(0.2),width=cms(0.4),fill='lightgrey', stroke='none').move_to(Point(cms(2.4),-cms(0.2))))


    def add_leds(self):
        for i in range(5):
            for j in range(5):
                self.add_led(i, j)

    def add_led(self, i, j):
        led_group_top_offset = cms(1.29)
        led_group_left_offset = cms(1.68)
        led_y_spacing = cms(0.4)
        led_x_spacing = cms(0.4)
        led_x = led_group_left_offset + i * led_x_spacing
        led_y = led_group_top_offset + j * led_y_spacing
        self.add(RectangularLed(Point(led_x, led_y)))

    def add_buttons(self):
        left_offset = cms(0.263)
        right_offset = cms(5.0-(0.625+0.263))
        distance_from_top = cms(1.9)
        self.add_button(left_offset, distance_from_top)
        self.add_button(right_offset, distance_from_top)

    def add_button_labels(self):
        self.add_label(Point(cms(0.619),cms(2.94)),'A', inverted=False)
        self.add_label(Point(cms(5.0-0.619),cms(1.5)),'B', inverted=True)

    def add_label(self, corner, text, inverted):
        scale = -1 if inverted else 1
        self.add(PolygonalPath(corner,
                               corner-Point(0, cms(0.32)).scale(scale),
                               corner-Point(cms(0.32),0).scale(scale), fill='teal'))
        if inverted:
            self.add(Text(text, corner+Point(cms(0.09),cms(0.16)), anchor='middle', size=5))
        else:
            self.add(Text(text, corner-Point(cms(0.1),cms(0.05)), anchor='middle', size=5))

    def add_decoration(self):
        self.add(Path(Point(0,cms(1.18)), vector(0, 4-cms(1.18)), arc(4,4,0,0,1,4,-4), vector(cms(1.18)-4, 0), fill='teal'))
        self.add(Path(Point(cms(1.18),0), vector(cms(0.6), 0), vector(cms(-0.6), cms(0.6)), fill='teal'))
        self.add(Path(Point(cms(1.18+0.6),0), vector(cms(0.21), 0), vector(cms(-0.21), cms(0.21)), fill='teal'))

    def add_logo(self):
        centre1, centre2 = (Point(cms(2.4),cms(0.82)),Point(cms(2.8),cms(0.82)))
        self.add(Path(centre1+Point(0,cms(0.15)),
                      arc(cms(0.15), cms(0.15), 0, 0, 1, 0, -cms(0.3)),vector(cms(0.4),0),
                      arc(cms(0.15), cms(0.15), 0, 0, 1, 0, cms(0.3)),fill='none',stroke='teal', width='2'))
        self.add(Circle(Point(0,0),cms(0.05), fill='teal').move_center_to(centre1))
        self.add(Circle(Point(0,0),cms(0.05), fill='teal').move_center_to(centre2))




