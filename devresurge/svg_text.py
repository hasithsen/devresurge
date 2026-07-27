"""Shared SVG text measurement helpers for embeddable badges.

Use a full-em advance so glyph width is never underestimated. Prefer wrapping
inside a capped canvas over a wide single line that panels clip.
"""

from __future__ import annotations

import html
import math
import re

_XML_SAFE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

# Full em advance — safe for Consolas/Menlo/Courier fallbacks under <img>.
_MONO_ADVANCE = 1.0
_SAFETY_PX = 20


def clean_text(value: str) -> str:
    return _XML_SAFE.sub("", (value or "").strip())


def xml_escape(value: str) -> str:
    return html.escape(clean_text(value), quote=False)


def text_width(text: str, font_size: float) -> float:
    return len(text) * font_size * _MONO_ADVANCE


def fit_canvas_width(
    *widths: float,
    pad_left: float,
    pad_right: float,
    min_width: int,
    max_width: int,
) -> int:
    content = max((w for w in widths if w is not None), default=0)
    needed = math.ceil(pad_left + content + pad_right + _SAFETY_PX)
    return int(min(max_width, max(min_width, needed)))


def wrap_by_chars(raw: str, *, max_chars: int) -> list[str]:
    """Word-wrap by character budget (font-agnostic, never ellipsizes)."""
    cleaned = clean_text(raw)
    if not cleaned:
        return []
    if max_chars < 8:
        max_chars = 8
    words = cleaned.split()
    if not words:
        return [cleaned]

    lines: list[str] = []
    current = ""
    for word in words:
        # Hard-break an oversized token rather than dropping it.
        while len(word) > max_chars:
            if current:
                lines.append(current)
                current = ""
            lines.append(word[:max_chars])
            word = word[max_chars:]
        if not word:
            continue
        candidate = word if not current else f"{current} {word}"
        if len(candidate) <= max_chars:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def wrap_words(
    raw: str,
    *,
    max_width: float,
    font_size: float,
    max_lines: int | None = None,
) -> list[str]:
    """Wrap using pixel budget derived from full-em advance."""
    max_chars = max(8, int(max_width // (font_size * _MONO_ADVANCE)))
    lines = wrap_by_chars(raw, max_chars=max_chars)
    if max_lines is not None and len(lines) > max_lines:
        kept = lines[:max_lines]
        # Ellipsize only the final kept line — never drop overflow silently.
        last = kept[-1]
        if len(last) + 1 > max_chars:
            last = last[: max(1, max_chars - 1)].rstrip() + "…"
        elif not last.endswith("…"):
            last = last.rstrip() + "…"
        kept[-1] = last
        return kept
    return lines


def fit_single_line(raw: str, *, max_width: float, font_size: float) -> str:
    cleaned = clean_text(raw)
    max_chars = max(8, int(max_width // (font_size * _MONO_ADVANCE)))
    if len(cleaned) <= max_chars:
        return xml_escape(cleaned)
    return xml_escape(cleaned[: max_chars - 1].rstrip() + "…")


def tspan_lines(
    lines: list[str],
    *,
    x: float,
    start_y: float,
    line_height: float,
    fill: str,
    font_size: float,
    font_weight: str = "400",
) -> str:
    weight_attr = f' font-weight="{font_weight}"' if font_weight != "400" else ""
    parts = []
    for i, line in enumerate(lines):
        y = start_y + i * line_height
        parts.append(
            f'<text x="{x}" y="{y}" fill="{fill}" font-size="{font_size}"{weight_attr} '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">'
            f"{xml_escape(line)}</text>",
        )
    return "\n  ".join(parts)
