# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Breadboarder is a Python DSL for describing breadboard-based electronics projects. It generates:
1. SVG diagrams of the circuit layout
2. Step-by-step assembly instructions in markdown

## Local Dependency

This project depends on a local `svg` library at `~/git/active/svg` (not published to PyPI). In PyCharm, this is attached as a project dependency.

## Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests (requires pytest.ini with pythonpath configured)
pytest

# Run specific test file
pytest src/python/breadboarder/tests/unit_tests/test_color_codes.py -v

# Run tests matching pattern
pytest -k "test_name_pattern" -v
```

The `pytest.ini` configures the Python path for both `breadboarder` and the `svg` dependency.

## Architecture

### Core Domain (`src/python/breadboarder/core/`)

- **project.py**: `Project` is the root container. It holds `Step` objects and uses the Visitor pattern (`welcome()` method) for processing. Steps can be `Part`, `Stage`, or `Note`.
- **host.py**: `Host` is a base class for things that have ports (sockets/pins) - like Breadboard and CP2102.
- **breadboard.py**: The `Breadboard` class with socket groups and power rails.
- **components.py**: Electronic components (`Wire`, `Resistor`, `LED`, `DIL`, etc.) that connect between ports.
- **port.py**: `Socket` and `Pin` classes representing connection points on hosts.

### Author/Publishing (`src/python/breadboarder/author/`, `publishing/`)

- **visitor.py**: `ProjectVisitor` abstract base class for the Visitor pattern.
- **illustrator.py**: `Illustrator` generates SVG by visiting project parts and collecting their SVG elements.
- **editor.py**: `Editor` orchestrates text and image output with options for when to insert pictures (per step, per stage, or at end).
- **book_maker.py**: `make_book()` is the main entry point for generating a complete publication.
- **pubwriters.py**: `FileBasedPublicationWriter` writes markdown and images to disk; `MockPublicationWriter` for testing.

### Helpers

- **color_codes.py**: Resistor color band encoding/decoding.
- **anns/layer.py**: Neural network diagram support (separate feature).

## Key Patterns

1. **Visitor Pattern**: Projects accept visitors (`Editor`, `Illustrator`) that process each step.

2. **Host/Port Model**: Hosts (Breadboard, CP2102) provide named ports accessed via `host['port_name']`. Components connect between ports.

3. **Component Hierarchy**: `Part` → `Component` → specific types (Wire, Resistor, LED, DIL). Each component knows how to draw itself and generate instructions.

## Typical Usage

```python
from breadboarder.core.project import Project
from breadboarder.core.breadboard import Breadboard
from breadboarder.core.components import Wire, Resistor
from svg.core import Point

project = Project()
breadboard = Breadboard().move_to(Point(20, 20))
project.add(breadboard)
project.add(Wire('red', breadboard['a1'], breadboard['j1']))
project.add(Resistor('10k', '5%', breadboard['a2'], breadboard['a7']))
```

## Test Structure

Tests are in `src/python/breadboarder/tests/`:
- `unit_tests/` - Unit tests
- `integration_tests/` - Integration tests
- `e2e_tests/` - End-to-end example scripts
- `helpers/` - Test utilities and mock objects
