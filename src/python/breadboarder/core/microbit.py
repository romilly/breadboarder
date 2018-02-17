from breadboarder.core.breadboard import Breadboard
from breadboarder.core.svg import GroupedDrawable, Rectangle, Point, Drawable, PolygonalPath, Text, Circle


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
    def __init__(self):
        GroupedDrawable.__init__(self, svg_id='microbit connector')
        self.wide_connector_start_positions = [1, 10, 19, 28, 35]
        self.add_end_connectors()
        self.add_wide_connectors()
        self.add_narrow_connectors()

    def wide_connector_spans(self):
        result = []
        for pos in self.wide_connector_start_positions:
            for i in range(4):
                result.append(pos+i)
        return result

    def add_end_connectors(self):
        self.add(PolygonalPath(Point(0, cms(-0.1)),Point(ins(0),cms(-0.54)),
                        Point(ins(0.05),cms(-0.54)),Point(ins(0.05),cms(0)),fill='gold'))
        self.add(PolygonalPath(Point(cms(5.1), cms(-0.1)),Point(cms(5.1),cms(-0.54)),
                        Point(cms(5.1)-ins(0.05),cms(-0.54)),Point(cms(5.1)-ins(0.05),cms(0)),fill='gold'))

    def add_wide_connectors(self):
        specs = zip(self.wide_connector_start_positions, ['0','1','2','3V','GND'])
        for spec in specs:
            self.add(self.wide_connector(*spec))

    def add_narrow_connectors(self):
        for i in set(range(40)) - (set([0,39]+self.wide_connector_spans())):
            self.add(Rectangle(ins(0.04),cms(0.54), fill='gold', stroke='none').move_to(Point(ins(0.009+i*0.05),cms(-0.54))))

    def wide_connector(self, pos, text):
        g = GroupedDrawable(text)
        g.add(Rectangle(ins(0.19),cms(0.65), fill='gold', stroke='none').move_to(Point(ins(0.009+pos*0.05),cms(-0.65))))
        g.add(Text(text, Point(ins(0.1+pos*0.05), cms(-0.2)),anchor='middle',size=6))
        g.add(Circle(Point(ins(-0.004+pos*0.05),cms(-0.95)),cms(0.27),fill='gold'))
        g.add(Circle(Point(ins(0.005+pos*0.05),cms(-0.92)),cms(0.245),fill='white'))
        return g


class Microbit(GroupedDrawable):
    def __init__(self):
        GroupedDrawable.__init__(self, svg_id='microbit')
        self.led_group_top_offset = cms(1.27)
        self.led_group_left_offset = cms(1.73)
        self.led_y_spacing = cms(0.4)
        self.led_x_spacing = cms(0.48)
        self.add_parts()

    def add_parts(self):
        self.add(Rectangle(height=cms(4.2), width=cms(5.1),rounded=True,fill='grey', stroke='none'))
        self.add_usb_port()
        self.add_leds()
        self.add_buttons()
        self.add(MicrobitConnector().move_to(Point(0, cms(4.2))))

    def add_usb_port(self):
        self.add(Rectangle(height=cms(0.2),width=cms(0.4),fill='lightgrey', stroke='none').move_to(Point(cms(2.4),-cms(0.2))))

    def add_leds(self):
        for i in range(5):
            for j in range(5):
                self.add_led(i, j)

    def add_buttons(self):
        pass


    def add_led(self, i, j):
        led_x = self.led_group_left_offset + i * self.led_x_spacing
        led_y = self.led_group_top_offset + j * self.led_y_spacing
        self.add(RectangularLed(Point(led_x, led_y)))



