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
