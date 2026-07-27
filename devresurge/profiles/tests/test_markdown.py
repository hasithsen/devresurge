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


def test_render_markdown_headings_lists_and_code():
    source = "# Title\n\n- one\n- two\n\n`code`\n\n```\nblock\n```"
    html = render_markdown(source)
    assert "<h1>Title</h1>" in html
    assert "<ul>" in html
    assert "<li>one</li>" in html
    assert "<code>code</code>" in html
    assert "<pre><code>block</code></pre>" in html


def test_render_markdown_empty():
    assert render_markdown("") == ""
    assert render_markdown("   ") == ""
