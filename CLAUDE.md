# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Breadboarder is a Python DSL for describing breadboard-based electronics projects. It generates:
1. SVG diagrams of the circuit layout
2. Step-by-step assembly instructions in markdown

## The svg Dependency

This project depends on the `svg` package from https://github.com/romilly/svg (distribution name `romilly-svg`; not on PyPI). Install it into the venv:

```bash
pip install git+https://github.com/romilly/svg      # or, to edit svg alongside:
pip install -e ~/git/active/svg
```

Don't add svg to `pytest.ini`'s `pythonpath`: the tests and `web/build.py` must import the same copy. Bump svg's version in its `pyproject.toml` with any change, or `pip install git+...` won't pick the change up.

## Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests (pytest.ini, which is local and untracked, adds src/python to the path)
pytest

# Browser editor tests (glue, build, and a check that the built page is up to date)
pytest web

# Rebuild the browser editor page after changing breadboarder, svg or web/
python web/build.py

# Run specific test file
pytest src/python/breadboarder/tests/unit_tests/test_color_codes.py -v

# Run tests matching pattern
pytest -k "test_name_pattern" -v
```

## Browser Editor (`web/`)

- **template.html**: the page. It loads Pyodide from a CDN and runs breadboarder in the browser.
- **glue.py**: the Python side. `render(code)` runs DSL code that defines `project` and returns the SVG, port positions and parts. `move(code, index, dx, dy)` rewrites the code when a part is dragged; it finds each part's source text by wrapping calls with `ast`.
- **build.py**: `build()` embeds the breadboarder and svg sources into `web/breadboarder-editor.html` (generated, git-ignored), along with a fingerprint of its sources; `is_up_to_date()` checks the fingerprint.
- **default_project.py**, **explorer_project.py**: example projects, offered in the page's Example menu. `EXAMPLES` in `build.py` lists them as (title, file); the first opens by default. To add one, add a file and an entry there.

The DSL code is the source of truth: the editor only edits the code, then re-runs it. The page runs the code on Run or Ctrl+Enter, after a drag or a new wire, and when an example is picked; not on typing.

## Versioning

Semantic versioning; the version is `__version__` in `src/python/breadboarder/__init__.py` and is shown in the editor's header. Bump it with each change.

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
from svg.point import Point

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
