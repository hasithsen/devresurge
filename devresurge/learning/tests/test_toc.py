from devresurge.learning.toc import lesson_headings
from devresurge.profiles.markdown import render_markdown


def test_lesson_headings_match_rendered_ids():
    body = "## First section\n\nText\n\n### Nested\n\nMore\n\n## Second"
    headings = lesson_headings(body)
    html = render_markdown(body, heading_ids=True)
    assert len(headings) == 3
    assert headings[0]["text"] == "First section"
    assert headings[1]["text"] == "Nested"
    for item in headings:
        assert f'id="{item["id"]}"' in html
