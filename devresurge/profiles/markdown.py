"""Safe, dependency-free Markdown subset for bios, lessons, and showcases.

Pipeline: split into blocks, then apply inline transforms (bold, links, …) on
text segments with HTML escaping. Links allow http(s), mailto, and same-site
paths starting with ``/``.
"""

from __future__ import annotations

import html
import re
from typing import Final

from django.utils.safestring import SafeString
from django.utils.safestring import mark_safe
from slugify import slugify

_ALLOWED_LINK_SCHEMES: Final = ("http://", "https://", "mailto:")

_RE_FENCE_OPEN = re.compile(r"^```([^\n`]*)$")
_RE_INLINE_CODE = re.compile(r"`([^`\n]+)`")
_RE_HEADING = re.compile(r"^(#{1,6})\s+(.+)$")
_RE_UL_ITEM = re.compile(r"^[\*\-]\s+(.+)$")
_RE_OL_ITEM = re.compile(r"^\d+\.\s+(.+)$")
_RE_BOLD = re.compile(r"\*\*(.+?)\*\*")
_RE_BOLD_UL = re.compile(r"__(.+?)__")
_RE_ITALIC = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")
_RE_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_RE_HR = re.compile(r"^(?:-{3,}|\*{3,}|_{3,})\s*$")
_RE_TABLE_ROW = re.compile(r"^\|.+\|$")
_RE_TABLE_SEP_CELL = re.compile(r"^:?-{1,}:?$")


def _normalize(source: str) -> str:
    return source.replace("\r\n", "\n").replace("\r", "\n")


def _safe_href(url: str) -> str | None:
    cleaned = html.unescape(url).strip()
    if not cleaned:
        return None
    lower = cleaned.lower()
    if cleaned.startswith("/") and not cleaned.startswith("//"):
        return html.escape(cleaned, quote=True)
    if not any(lower.startswith(scheme) for scheme in _ALLOWED_LINK_SCHEMES):
        return None
    if ":" in lower.split("://", 1)[0] and not lower.startswith("mailto:"):
        if not lower.startswith(("http://", "https://")):
            return None
    return html.escape(cleaned, quote=True)


def _inline(text: str, *, links: bool = True) -> str:
    """Apply inline Markdown to a plain-text segment (escaped before output)."""
    placeholders: list[str] = []

    def stash(fragment: str) -> str:
        placeholders.append(fragment)
        return f"\x00PH{len(placeholders) - 1}\x00"

    escaped = html.escape(text)

    def inline_code_sub(match: re.Match[str]) -> str:
        return stash(f"<code>{match.group(1)}</code>")

    escaped = _RE_INLINE_CODE.sub(inline_code_sub, escaped)

    if links:

        def link_sub(match: re.Match[str]) -> str:
            raw_label, raw_url = match.group(1), match.group(2)
            href = _safe_href(raw_url)
            label = _inline(raw_label, links=False)
            if href is None:
                return label
            return (
                f'<a href="{href}" rel="noopener nofollow ugc" target="_blank">'
                f"{label}</a>"
            )

        escaped = _RE_LINK.sub(link_sub, escaped)

    escaped = _RE_BOLD.sub(r"<strong>\1</strong>", escaped)
    escaped = _RE_BOLD_UL.sub(r"<strong>\1</strong>", escaped)
    escaped = _RE_ITALIC.sub(r"<em>\1</em>", escaped)

    for idx, fragment in enumerate(placeholders):
        escaped = escaped.replace(f"\x00PH{idx}\x00", fragment)
    return escaped


def _heading_anchor(text: str, seen: dict[str, int]) -> str:
    plain = re.sub(r"<[^>]+>", "", text)
    base = slugify(plain)[:80] or "section"
    count = seen.get(base, 0)
    seen[base] = count + 1
    return base if count == 0 else f"{base}-{count}"


def _render_heading(line: str, *, heading_ids: bool, seen: dict[str, int]) -> str:
    match = _RE_HEADING.match(line)
    if not match:
        return f"<p>{_inline(line)}</p>"
    level = len(match.group(1))
    inner = _inline(match.group(2).strip())
    if heading_ids and level >= 2:
        anchor = html.escape(_heading_anchor(match.group(2).strip(), seen), quote=True)
        return f'<h{level} id="{anchor}">{inner}</h{level}>'
    return f"<h{level}>{inner}</h{level}>"


def _render_list(lines: list[str], *, ordered: bool) -> str:
    pattern = _RE_OL_ITEM if ordered else _RE_UL_ITEM
    items: list[str] = []
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
        items.append(f"<li>{_inline(match.group(1).strip())}</li>")
    if not items:
        return ""
    tag = "ol" if ordered else "ul"
    return f"<{tag}>{''.join(items)}</{tag}>"


def _parse_table_cells(line: str) -> list[str]:
    inner = line.strip()
    if not inner.startswith("|"):
        return []
    if inner.endswith("|"):
        inner = inner[1:-1]
    else:
        inner = inner[1:]
    return [cell.strip() for cell in inner.split("|")]


def _is_table_separator(cells: list[str]) -> bool:
    if not cells:
        return False
    return all(_RE_TABLE_SEP_CELL.match(cell.strip()) for cell in cells if cell.strip())


def _render_table(lines: list[str]) -> str:
    rows: list[list[str]] = []
    for line in lines:
        cells = _parse_table_cells(line)
        if cells:
            rows.append(cells)
    if not rows:
        return ""

    header_html = ""
    body_rows = rows
    if len(rows) >= 2 and _is_table_separator(rows[1]):
        header_cells = "".join(f'<th scope="col">{_inline(c)}</th>' for c in rows[0])
        header_html = f"<thead><tr>{header_cells}</tr></thead>"
        body_rows = rows[2:]

    body_html = "".join(
        "<tr>" + "".join(f"<td>{_inline(cell)}</td>" for cell in row) + "</tr>"
        for row in body_rows
    )
    return (
        '<div class="dr-table-wrap"><table class="dr-table dr-table--markdown">'
        f"{header_html}<tbody>{body_html}</tbody></table></div>"
    )


def _render_blockquote(lines: list[str]) -> str:
    parts: list[str] = []
    for line in lines:
        text = line.lstrip(">").lstrip()
        if text:
            parts.append(_inline(text))
    inner = "<br />".join(parts) if len(parts) > 1 else (parts[0] if parts else "")
    return f"<blockquote class=\"dr-markdown-quote\">{inner}</blockquote>"


def _is_table_line(line: str) -> bool:
    return bool(_RE_TABLE_ROW.match(line.strip()))


def _is_list_line(line: str) -> bool:
    return bool(_RE_UL_ITEM.match(line) or _RE_OL_ITEM.match(line))


def _list_kind(line: str) -> str | None:
    if _RE_OL_ITEM.match(line):
        return "ol"
    if _RE_UL_ITEM.match(line):
        return "ul"
    return None


def render_markdown(source: str, *, heading_ids: bool = False) -> SafeString:
    """Render a bio-safe Markdown subset to HTML."""
    if not source or not source.strip():
        return mark_safe("")  # noqa: S308 — empty string is safe

    text = _normalize(source)
    lines = text.split("\n")
    heading_seen: dict[str, int] = {}
    blocks: list[str] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        fence = _RE_FENCE_OPEN.match(stripped)
        if fence:
            lang = fence.group(1).strip()
            i += 1
            body_lines: list[str] = []
            while i < n and not lines[i].strip().startswith("```"):
                body_lines.append(html.escape(lines[i]))
                i += 1
            if i < n:
                i += 1
            lang_attr = f' class="language-{html.escape(lang, quote=True)}"' if lang else ""
            body = "\n".join(body_lines)
            blocks.append(f"<pre><code{lang_attr}>{body}</code></pre>")
            continue

        if _RE_HEADING.match(stripped):
            blocks.append(_render_heading(stripped, heading_ids=heading_ids, seen=heading_seen))
            i += 1
            continue

        if _RE_HR.match(stripped):
            blocks.append('<hr class="dr-markdown-hr" />')
            i += 1
            continue

        if _is_table_line(stripped):
            table_lines: list[str] = []
            while i < n and _is_table_line(lines[i].strip()):
                table_lines.append(lines[i].strip())
                i += 1
            table_html = _render_table(table_lines)
            if table_html:
                blocks.append(table_html)
            continue

        if stripped.startswith(">"):
            quote_lines: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip())
                i += 1
            blocks.append(_render_blockquote(quote_lines))
            continue

        list_kind = _list_kind(stripped)
        if list_kind:
            list_lines: list[str] = []
            while i < n and _list_kind(lines[i].strip()) == list_kind:
                list_lines.append(lines[i].strip())
                i += 1
            list_html = _render_list(list_lines, ordered=list_kind == "ol")
            if list_html:
                blocks.append(list_html)
            continue

        para_lines: list[str] = [stripped]
        i += 1
        while i < n:
            nxt = lines[i].strip()
            if not nxt:
                break
            if (
                _RE_FENCE_OPEN.match(nxt)
                or _RE_HEADING.match(nxt)
                or _RE_HR.match(nxt)
                or _is_table_line(nxt)
                or nxt.startswith(">")
                or _is_list_line(nxt)
            ):
                break
            para_lines.append(nxt)
            i += 1
        inner = _inline("\n".join(para_lines)).replace("\n", "<br />")
        blocks.append(f"<p>{inner}</p>")

    return mark_safe("\n".join(blocks))  # noqa: S308 — built from escaped + safe tags
