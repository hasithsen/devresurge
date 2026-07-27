"""Safe, dependency-free Markdown subset for profile bios.

Pipeline: escape HTML first, then apply a fixed set of substitutions that
only emit known-safe tags. Links are restricted to http(s)/mailto and
always carry ``rel="noopener nofollow ugc"``.
"""

from __future__ import annotations

import html
import re
from typing import Final

from django.utils.safestring import SafeString
from django.utils.safestring import mark_safe

_ALLOWED_LINK_SCHEMES: Final = ("http://", "https://", "mailto:")

_RE_CODE_BLOCK = re.compile(r"```([^\n`]*)\n(.*?)```", re.DOTALL)
_RE_INLINE_CODE = re.compile(r"`([^`\n]+)`")
_RE_HEADING = re.compile(r"^(#{1,3})\s+(.+)$", re.MULTILINE)
_RE_UL_BLOCK = re.compile(r"(?:^[\*\-]\s+.+(?:\n|$))+", re.MULTILINE)
_RE_OL_BLOCK = re.compile(r"(?:^\d+\.\s+.+(?:\n|$))+", re.MULTILINE)
_RE_UL_ITEM = re.compile(r"^[\*\-]\s+(.+)$", re.MULTILINE)
_RE_OL_ITEM = re.compile(r"^\d+\.\s+(.+)$", re.MULTILINE)
_RE_BOLD = re.compile(r"\*\*(.+?)\*\*")
_RE_ITALIC = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")
_RE_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_RE_PARA_SPLIT = re.compile(r"\n{2,}")


def _safe_href(url: str) -> str | None:
    cleaned = html.unescape(url).strip()
    lower = cleaned.lower()
    if not any(lower.startswith(scheme) for scheme in _ALLOWED_LINK_SCHEMES):
        return None
    # Block javascript:/data: even if somehow prefixed.
    if ":" in lower.split("://", 1)[0] and not lower.startswith("mailto:"):
        if not lower.startswith(("http://", "https://")):
            return None
    return html.escape(cleaned, quote=True)


def _inline(text: str) -> str:
    """Apply inline Markdown transforms to already-escaped text."""

    def link_sub(match: re.Match[str]) -> str:
        label, raw_url = match.group(1), match.group(2)
        href = _safe_href(raw_url)
        if href is None:
            return label
        return (
            f'<a href="{href}" rel="noopener nofollow ugc" target="_blank">'
            f"{label}</a>"
        )

    text = _RE_LINK.sub(link_sub, text)
    text = _RE_BOLD.sub(r"<strong>\1</strong>", text)
    text = _RE_ITALIC.sub(r"<em>\1</em>", text)
    return text


def _render_list(block: str, *, ordered: bool) -> str:
    pattern = _RE_OL_ITEM if ordered else _RE_UL_ITEM
    items = "".join(f"<li>{_inline(m.group(1).strip())}</li>" for m in pattern.finditer(block))
    tag = "ol" if ordered else "ul"
    return f"<{tag}>{items}</{tag}>"


def render_markdown(source: str) -> SafeString:
    """Render a bio-safe Markdown subset to HTML.

    Supports: headings (h1–h3), fenced code blocks, inline code, bold,
    italic, links (http/https/mailto), unordered + ordered lists, and
    paragraphs. Everything else is escaped as plain text.
    """
    if not source or not source.strip():
        return mark_safe("")  # noqa: S308 — empty string is safe

    # Placeholders keep code spans out of later transforms.
    placeholders: list[str] = []

    def stash(html_fragment: str) -> str:
        placeholders.append(html_fragment)
        return f"\x00PH{len(placeholders) - 1}\x00"

    escaped = html.escape(source)

    def code_block_sub(match: re.Match[str]) -> str:
        body = match.group(2).rstrip("\n")
        return stash(f"<pre><code>{body}</code></pre>")

    escaped = _RE_CODE_BLOCK.sub(code_block_sub, escaped)

    def inline_code_sub(match: re.Match[str]) -> str:
        return stash(f"<code>{match.group(1)}</code>")

    escaped = _RE_INLINE_CODE.sub(inline_code_sub, escaped)

    def heading_sub(match: re.Match[str]) -> str:
        level = len(match.group(1))
        return f"<h{level}>{_inline(match.group(2).strip())}</h{level}>"

    escaped = _RE_HEADING.sub(heading_sub, escaped)
    escaped = _RE_UL_BLOCK.sub(lambda m: _render_list(m.group(0), ordered=False), escaped)
    escaped = _RE_OL_BLOCK.sub(lambda m: _render_list(m.group(0), ordered=True), escaped)

    parts: list[str] = []
    for chunk in _RE_PARA_SPLIT.split(escaped.strip()):
        chunk = chunk.strip()
        if not chunk:
            continue
        # Already a block element — don't wrap in <p>.
        if chunk.startswith(("<h1", "<h2", "<h3", "<ul", "<ol", "\x00PH")):
            parts.append(_inline(chunk) if not chunk.startswith("\x00PH") else chunk)
        else:
            parts.append(f"<p>{_inline(chunk.replace(chr(10), '<br />'))}</p>")

    html_out = "\n".join(parts)
    for idx, fragment in enumerate(placeholders):
        html_out = html_out.replace(f"\x00PH{idx}\x00", fragment)

    return mark_safe(html_out)  # noqa: S308 — built from escaped + safe tags
