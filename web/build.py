"""Build breadboarder-editor.html: a single page that runs breadboarder in Pyodide.

The page embeds the breadboarder and svg package sources, so it can be opened
straight from disk or published anywhere. From a notebook:

    import sys; sys.path.insert(0, 'web')
    import build; build.build()
"""
import json
import pathlib

import svg

WEB = pathlib.Path(__file__).resolve().parent
BREADBOARDER = WEB.parent / 'src' / 'python' / 'breadboarder'
SVG = pathlib.Path(svg.__file__).resolve().parent


def package_sources(root, skip=()):
    return {str(pathlib.Path(root.name) / p.relative_to(root)): p.read_text()
            for p in sorted(root.rglob('*.py'))
            if not any(part in skip for part in p.relative_to(root).parts)}


def as_js(value):
    return json.dumps(value).replace('</', '<\\/')


def build(output=WEB / 'breadboarder-editor.html'):
    files = {**package_sources(BREADBOARDER, skip={'tests'}), **package_sources(SVG)}
    html = (WEB / 'template.html').read_text()
    html = (html.replace('__FILES__', as_js(files))
                .replace('__GLUE__', as_js((WEB / 'glue.py').read_text()))
                .replace('__DEFAULT_CODE__', as_js((WEB / 'default_project.py').read_text())))
    pathlib.Path(output).write_text(html)
    return output


if __name__ == '__main__':
    print(build())
