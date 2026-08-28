"""In-lesson table of contents from markdown headings."""

from __future__ import annotations

import re

from slugify import slugify

_HEADING = re.compile(r"^(#{2,3})\s+(.+)$")


def lesson_headings(source: str) -> list[dict[str, str | int]]:
    """Extract h2/h3 anchors for a lesson TOC (matches render_markdown ids)."""
    seen: dict[str, int] = {}
    items: list[dict[str, str | int]] = []
    for line in (source or "").splitlines():
        match = _HEADING.match(line.strip())
        if not match:
            continue
        level = len(match.group(1))
        text = match.group(2).strip()
        base = slugify(text)[:80] or "section"
        count = seen.get(base, 0)
        seen[base] = count + 1
        anchor = base if count == 0 else f"{base}-{count}"
        items.append({"level": level, "text": text, "id": anchor})
    return items
