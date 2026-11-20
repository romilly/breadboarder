import json
import pathlib
import sys

import pytest

WEB = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(WEB.parent / 'src' / 'python'))
sys.path.insert(0, str(WEB))

import glue  # noqa: E402

CODE = (WEB / 'default_project.py').read_text()
PITCH = 9


def parts(code=CODE):
    return json.loads(glue.render(code))['parts']


def index_of(kind_name, code=CODE):
    return [p['name'] for p in parts(code)].index(kind_name)


def test_render_lists_parts_in_drawing_order():
    names = [p['name'] for p in parts()]
    assert names[:3] == ['Breadboard', 'CP2102', 'Wire']
    assert parts()[0]['kind'] == 'host'
    assert parts()[2]['kind'] == 'component'


def test_moving_a_host_rewrites_its_move_to():
    new = glue.move(CODE, 0, 10.4, -5)
    assert "breadboard = Breadboard().move_to(Point(30, 15))" in new


def test_moving_a_rotated_host_changes_only_move_to():
    # after rotate(-90), move_to works in the rotated frame: +y there is +x on screen
    new = glue.move(CODE, 1, 5, 0)
    assert "CP2102().rotate(-90., Point(40, 400)).move_to(Point(40, 405))" in new


def port_positions(code, host):
    ns, _ = glue._run(code)
    return {name: (p.location().x, p.location().y) for name, p in ns[host]._ports.items()}


@pytest.mark.parametrize('host, index', [('breadboard', 0), ('cp', 1)])
def test_dragged_host_ports_move_by_the_drag(host, index):
    before = port_positions(CODE, host)
    after = port_positions(glue.move(CODE, index, 20, -10), host)
    for name, (x, y) in before.items():
        assert after[name] == pytest.approx((x + 20, y - 10))


def test_moving_a_host_without_move_to_adds_one():
    code = CODE.replace("Breadboard().move_to(Point(20, 20))", "Breadboard()")
    new = glue.move(code, 0, 20, 20)
    assert "Breadboard().move_to(Point(20, 20))" in new


def test_moving_a_component_snaps_to_new_sockets():
    i = index_of('Resistor')
    new = glue.move(CODE, i, PITCH + 2, -1)
    assert "Resistor('10k', '5%', breadboard['b4'], breadboard['b10'])" in new


def test_moving_a_dil_chip_by_two_columns():
    i = index_of('DIL')
    new = glue.move(CODE, i, 2 * PITCH, 0)
    assert "atMega328(breadboard['f5'])" in new


def test_moving_a_wire_end_off_the_end_of_a_header_is_refused():
    i = index_of('Wire')  # cp['GND'] is the last pin on the header
    with pytest.raises(ValueError):
        glue.move(CODE, i, 2 * PITCH, 0)


def test_a_wire_can_slide_along_a_header():
    i = index_of('Wire')
    new = glue.move(CODE, i, -PITCH, 0)
    assert "Wire('green', cp['CTS'], breadboard['a9'])" in new


def test_moving_off_the_board_is_refused():
    i = index_of('Resistor')
    with pytest.raises(ValueError):
        glue.move(CODE, i, -10 * PITCH, 0)


def test_tiny_component_move_leaves_code_unchanged():
    i = index_of('Resistor')
    assert glue.move(CODE, i, 2, 2) == CODE


def test_explorer_example_draws_an_explorer():
    example = (WEB / 'explorer_project.py').read_text()
    assert parts(example)[0]['name'] == 'Explorer'


EXPLORER_CODE = """\
from breadboarder.core.project import Project
from breadboarder.core.explorer import Explorer
from breadboarder.core.components import Wire, Resistor
from svg.point import Point

project = Project()
explorer = Explorer().move_to(Point(60, 60))
project.add(explorer,
            Resistor('220R', '5%', explorer['a1'], explorer['a5']),
            Wire('red', explorer['GP0'], explorer['e1']))
"""


def test_render_reports_explorer_ports():
    ports = json.loads(glue.render(EXPLORER_CODE))['ports']
    names = {port_name for host, port_name, x, y in ports if host == 'explorer'}
    assert {'GP0', 'GND2', 'a1', 'j17', 'PAD_3V3', 'PAD_GND_L'} <= names


def test_moving_a_component_on_the_explorer_snaps_to_its_sockets():
    i = index_of('Resistor', EXPLORER_CODE)
    new = glue.move(EXPLORER_CODE, i, PITCH, 0)
    assert "Resistor('220R', '5%', explorer['a2'], explorer['a6'])" in new


def test_palette_lists_two_pin_parts_with_port_counts():
    palette = json.loads(glue.palette())
    kinds = {entry['kind']: entry for entry in palette}
    assert kinds['Wire']['ports'] == 2
    assert {'Wire', 'Resistor', 'LED', 'Diode', 'DiskCapacitor', 'Crystal'} <= set(kinds)
    assert all(entry['label'] for entry in palette)


def test_add_part_appends_a_project_add_line():
    new = glue.add_part(CODE, 'Resistor', ["breadboard['a20']", "breadboard['a24']"])
    assert new.rstrip().endswith("project.add(Resistor('10k', '5%', breadboard['a20'], breadboard['a24']))")


def test_add_wire_uses_the_chosen_colour():
    new = glue.add_part(CODE, 'Wire', ["breadboard['d9']", "breadboard['g11']"], colour='blue')
    assert "project.add(Wire('blue', breadboard['d9'], breadboard['g11']))" in new


def test_add_part_imports_its_class_when_needed():
    assert 'Diode' not in CODE
    new = glue.add_part(CODE, 'Diode', ["breadboard['a20']", "breadboard['a24']"])
    assert 'from breadboarder.core.components import Diode\n' in new
    # next to the existing import from the same module, not after svg's
    assert new.index('import Diode') < new.index('from svg.point')
    names = [p['name'] for p in json.loads(glue.render(new))['parts']]
    assert names[-1] == 'Diode'


def test_add_part_does_not_repeat_an_existing_import():
    new = glue.add_part(CODE, 'LED', ["breadboard['a20']", "breadboard['a24']"])
    assert new.count('import') == CODE.count('import')


def test_add_part_with_the_wrong_number_of_ports_is_refused():
    with pytest.raises(ValueError):
        glue.add_part(CODE, 'Resistor', ["breadboard['a20']"])


def test_palette_offers_one_port_parts():
    kinds = {e['kind']: e for e in json.loads(glue.palette())}
    assert kinds['atMega328']['ports'] == 1
    assert kinds['pcf8574']['ports'] == 1
    assert kinds['header6']['ports'] == 1


def test_add_a_chip_straddling_the_centre():
    new = glue.add_part(CODE, 'atMega328', ["breadboard['f10']"])
    assert new.rstrip().endswith("project.add(atMega328(breadboard['f10']))")


def test_chip_running_off_the_end_of_the_board_is_refused():
    with pytest.raises(ValueError):
        glue.add_part(CODE, 'atMega328', ["breadboard['f20']"])  # 14 pins per side from column 20


def test_chip_not_straddling_the_centre_is_refused():
    with pytest.raises(ValueError):
        glue.add_part(CODE, 'atMega328', ["breadboard['a10']"])


def test_header_uses_the_header_function_and_imports_it():
    new = glue.add_part(CODE, 'header6', ["breadboard['a1']"])
    assert 'from breadboarder.core.header import header\n' in new
    assert new.rstrip().endswith("project.add(header(6, breadboard['a1']))")
    assert json.loads(glue.render(new))['parts'][-1]['name'] == 'Header'


def test_header_off_the_end_is_refused():
    with pytest.raises(ValueError):
        glue.add_part(CODE, 'header6', ["breadboard['a27']"])


def test_preview_draws_the_part_and_says_whether_it_fits():
    good = json.loads(glue.preview(CODE, 'pcf8574', "breadboard['f20']"))
    assert good['ok'] and good['svg'].startswith('<g')
    bad = json.loads(glue.preview(CODE, 'pcf8574', "breadboard['f25']"))
    assert not bad['ok'] and bad['message']
    assert bad['svg'].startswith('<g')
