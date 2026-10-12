"""Filesystem course index with path-traversal-safe resolution."""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from django.conf import settings

_HEADING_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


@dataclass(frozen=True)
class CourseDoc:
    course_slug: str
    chapter_slug: str
    title: str
    summary: str
    path: str  # relative posix path under courses/
    order: int


def courses_root() -> Path:
    configured = getattr(settings, "SEARCH_COURSES_ROOT", None)
    if configured:
        return Path(configured).resolve()
    return (Path(settings.BASE_DIR) / "courses").resolve()


def _safe_under_root(root: Path, candidate: Path) -> Path | None:
    try:
        resolved = candidate.resolve()
        resolved.relative_to(root)
    except (OSError, ValueError):
        return None
    if not resolved.is_file() or resolved.suffix.lower() != ".md":
        return None
    return resolved


def resolve_course_file(course_slug: str, chapter_slug: str | None = None) -> Path | None:
    """Resolve a course markdown file; rejects path traversal."""
    root = courses_root()
    if not _safe_slug(course_slug):
        return None
    if chapter_slug is None:
        for name in ("00-README.md", "README.md"):
            hit = _safe_under_root(root, root / course_slug / name)
            if hit is not None:
                return hit
        return None
    if not _safe_slug(chapter_slug):
        return None
    # Allow optional numeric prefix already in slug, or exact filename.
    direct = _safe_under_root(root, root / course_slug / f"{chapter_slug}.md")
    if direct is not None:
        return direct
    # Match files like 01-linux-processes.md when chapter_slug is linux-processes
    course_dir = root / course_slug
    if not course_dir.is_dir():
        return None
    for path in sorted(course_dir.glob("*.md")):
        stem = path.stem
        bare = re.sub(r"^\d+-", "", stem)
        if stem == chapter_slug or bare == chapter_slug:
            return _safe_under_root(root, path)
    return None


def _safe_slug(value: str) -> bool:
    return bool(value) and bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,120}", value))


def _title_and_summary(text: str, fallback: str) -> tuple[str, str]:
    match = _HEADING_RE.search(text)
    title = match.group(1).strip() if match else fallback
    # First non-empty, non-heading, non-fence line as summary
    summary = ""
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("```"):
            continue
        if stripped.startswith(">") or stripped.startswith("|") or stripped.startswith("---"):
            continue
        summary = _MD_LINK_RE.sub(r"\1", stripped)
        summary = re.sub(r"[*`_]", "", summary)
        break
    return title, summary[:180]


@lru_cache(maxsize=1)
def build_course_index() -> tuple[CourseDoc, ...]:
    root = courses_root()
    if not root.is_dir():
        return ()
    docs: list[CourseDoc] = []
    order = 0
    for course_dir in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")):
        if not _safe_slug(course_dir.name):
            continue
        for path in sorted(course_dir.glob("*.md")):
            if path.name.lower() == "readme.md" and not path.name.startswith("00"):
                # Prefer 00-README when both exist; still index bare README if alone.
                if (course_dir / "00-README.md").is_file():
                    continue
            try:
                text = path.read_text(encoding="utf-8")
            except OSError:
                continue
            title, summary = _title_and_summary(text, path.stem)
            chapter_slug = path.stem
            docs.append(
                CourseDoc(
                    course_slug=course_dir.name,
                    chapter_slug=chapter_slug,
                    title=title,
                    summary=summary,
                    path=f"{course_dir.name}/{path.name}",
                    order=order,
                ),
            )
            order += 1
    return tuple(docs)


def list_course_slugs() -> list[str]:
    root = courses_root()
    if not root.is_dir():
        return []
    return sorted(
        p.name
        for p in root.iterdir()
        if p.is_dir() and not p.name.startswith(".") and _safe_slug(p.name)
    )


def clear_course_index_cache() -> None:
    build_course_index.cache_clear()
