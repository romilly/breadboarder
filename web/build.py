"""Build breadboarder-editor.html: a single page that runs breadboarder in Pyodide.

The page embeds the breadboarder and svg package sources, so it can be opened
straight from disk or published anywhere. From a notebook:

    import sys; sys.path.insert(0, 'web')
    import build; build.build()

The page records a fingerprint of everything it was built from;
build.is_up_to_date() says whether it still matches the sources.
"""
import hashlib
import json
import pathlib
import re

import svg

WEB = pathlib.Path(__file__).resolve().parent
BREADBOARDER = WEB.parent / 'src' / 'python' / 'breadboarder'
SVG = pathlib.Path(svg.__file__).resolve().parent
OUTPUT = WEB / 'breadboarder-editor.html'
# (title, file) for the page's Example menu; the first opens by default
EXAMPLES = (('CP2102 and ATmega328', 'default_project.py'),
            ('Pimoroni Explorer', 'explorer_project.py'))
WEB_SOURCES = ('template.html', 'glue.py', 'build.py') + tuple(name for _, name in EXAMPLES)
FINGERPRINT_TAG = re.compile(r'<meta name="breadboarder-build" content="([0-9a-f]+)">')


def package_sources(root, skip=()):
    return {str(pathlib.Path(root.name) / p.relative_to(root)): p.read_text()
            for p in sorted(root.rglob('*.py'))
            if not any(part in skip for part in p.relative_to(root).parts)}


def packages():
    return {**package_sources(BREADBOARDER, skip={'tests'}), **package_sources(SVG)}


def version():
    text = (BREADBOARDER / '__init__.py').read_text()
    return re.search(r"""__version__\s*=\s*['"]([^'"]+)['"]""", text).group(1)


def fingerprint():
    """SHA-256 of every file the page is built from."""
    sources = {**packages(), **{'web/' + name: (WEB / name).read_text() for name in WEB_SOURCES}}
    digest = hashlib.sha256()
    for path in sorted(sources):
        digest.update(path.encode() + b'\0' + sources[path].encode() + b'\0')
    return digest.hexdigest()


def is_up_to_date(output=OUTPUT):
    output = pathlib.Path(output)
    if not output.exists():
        return False
    match = FINGERPRINT_TAG.search(output.read_text())
    return bool(match) and match.group(1) == fingerprint()


def as_js(value):
    return json.dumps(value).replace('</', '<\\/')


def build(output=OUTPUT):
    full = fingerprint()
    html = (WEB / 'template.html').read_text()
    html = (html.replace('__FINGERPRINT__', full)
                .replace('__VERSION__', version())
                .replace('__BUILD__', full[:7])
                .replace('__FILES__', as_js(packages()))
                .replace('__GLUE__', as_js((WEB / 'glue.py').read_text()))
                .replace('__EXAMPLES__', as_js([[title, (WEB / name).read_text()]
                                                for title, name in EXAMPLES])))
    output = pathlib.Path(output)
    output.write_text(html)
    return output


if __name__ == '__main__':
    print(build())
