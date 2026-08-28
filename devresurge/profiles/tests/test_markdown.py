from __future__ import annotations

from devresurge.profiles.markdown import render_markdown


def test_render_markdown_escapes_raw_html():
    html = render_markdown("<script>alert(1)</script> **ok**")
    assert "<script>" not in html
    assert "&lt;script&gt;" in html
    assert "<strong>ok</strong>" in html


def test_render_markdown_allows_safe_links_only():
    html = render_markdown("[safe](https://example.com) [bad](javascript:alert(1))")
    assert 'href="https://example.com"' in html
    assert "javascript:" not in html
    assert "bad" in html


def test_render_markdown_same_site_relative_links():
    html = render_markdown(
        "[Data sprint](/learn/data-science-interview/) and "
        "[quiz](/quizzes/sql-fundamentals/).",
    )
    assert 'href="/learn/data-science-interview/"' in html
    assert 'href="/quizzes/sql-fundamentals/"' in html


def test_render_markdown_headings_lists_and_code():
    source = "# Title\n\n- one\n- two\n\n`code`\n\n```\nblock\n```"
    html = render_markdown(source)
    assert "<h1>Title</h1>" in html
    assert "<ul>" in html
    assert "<li>one</li>" in html
    assert "<code>code</code>" in html
    assert "<pre><code>block</code></pre>" in html


def test_render_markdown_bold_in_list_and_paragraph():
    source = (
        "- **Medallion:** bronze\n\n"
        "**Optional:** complete [elective](/learn/data-fundamentals-elective/) if rusty.\n\n"
        "**Role clarity:** owns **reliable** systems"
    )
    html = render_markdown(source)
    assert "<li><strong>Medallion:</strong> bronze</li>" in html
    assert "<strong>Optional:</strong>" in html
    assert 'href="/learn/data-fundamentals-elective/"' in html
    assert html.count("<strong>") >= 4


def test_render_markdown_tables():
    source = """| Platform | Points |
|----------|--------|
| Snowflake | **Virtual** warehouses |
| BigQuery | Partitioning |"""
    html = render_markdown(source)
    assert "<table" in html
    assert "<thead>" in html
    assert "<th" in html and "Platform" in html
    assert "<strong>Virtual</strong>" in html
    assert "BigQuery" in html


def test_render_markdown_blockquote_with_bold():
    source = "> Not legal advice. Verify with **official** sources."
    html = render_markdown(source)
    assert "<blockquote" in html
    assert "<strong>official</strong>" in html
    assert "&gt;" not in html


def test_render_markdown_heading_ids():
    source = "## First\n\n### Nested\n\n## Second"
    html = render_markdown(source, heading_ids=True)
    assert 'id="first"' in html
    assert 'id="nested"' in html
    assert 'id="second"' in html


def test_render_markdown_empty():
    assert render_markdown("") == ""
    assert render_markdown("   ") == ""
