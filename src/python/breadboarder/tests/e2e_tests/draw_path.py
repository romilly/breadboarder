from breadboarder.core.project import Project
from breadboarder.core.svg import PolygonalPath, Point, write


def test_path():
    project = Project()
    path = PolygonalPath(Point(0,0), Point(0,10), Point(10,15), Point(10, 0))
    project.add(path)
    svg = project.element()
    write(svg, 'svg/poly.svg')

test_path()

