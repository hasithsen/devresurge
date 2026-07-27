from __future__ import annotations

from django import template
from django.utils.safestring import SafeString

from devresurge.profiles.markdown import render_markdown

register = template.Library()


@register.filter(name="markdownify")
def markdownify(value: str | None) -> SafeString:
    """Render a safe Markdown subset to HTML for profile bios."""
    return render_markdown(value or "")
