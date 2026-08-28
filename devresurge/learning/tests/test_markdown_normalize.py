from devresurge.learning.catalog import normalize_lesson_markdown


def test_normalize_collapses_extra_blank_lines():
    raw = "## Title\n\n\n\nParagraph one.\n\n\nParagraph two.\n  \n"
    assert normalize_lesson_markdown(raw) == "## Title\n\nParagraph one.\n\nParagraph two."


def test_normalize_strips_trailing_line_whitespace():
    raw = "- item with spaces   \n- another  "
    assert normalize_lesson_markdown(raw) == "- item with spaces\n- another"
