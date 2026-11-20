import pathlib
import re
import sys

import pytest

WEB = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(WEB))

import build  # noqa: E402

SEMVER = re.compile(r'^\d+\.\d+\.\d+$')


def test_version_is_semantic():
    assert SEMVER.match(build.version())


def test_page_shows_version_and_fingerprint(tmp_path):
    page = build.build(tmp_path / 'editor.html').read_text()
    assert build.version() in page
    assert build.fingerprint()[:7] in page


def test_page_offers_each_example(tmp_path):
    page = build.build(tmp_path / 'editor.html').read_text()
    for title, filename in build.EXAMPLES:
        assert title in page
        assert build.as_js((build.WEB / filename).read_text()) in page


def test_fresh_build_is_up_to_date(tmp_path):
    output = build.build(tmp_path / 'editor.html')
    assert build.is_up_to_date(output)


def test_changed_sources_make_the_page_stale(tmp_path):
    output = build.build(tmp_path / 'editor.html')
    text = output.read_text().replace(build.fingerprint(), '0' * 64)
    output.write_text(text)
    assert not build.is_up_to_date(output)


def test_missing_page_is_not_up_to_date(tmp_path):
    assert not build.is_up_to_date(tmp_path / 'nothing.html')


def test_built_page_is_up_to_date():
    """Fails if web/breadboarder-editor.html needs rebuilding."""
    if not build.OUTPUT.exists():
        pytest.skip('page not built yet')
    assert build.is_up_to_date(), 'The editor page is stale: run python web/build.py'
