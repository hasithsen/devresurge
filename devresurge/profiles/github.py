"""Fetch public GitHub file contents for profile showcases.

Public repos only — no OAuth. Uses the Contents API and raw URLs with
strict host allowlists, size caps, and timeouts.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.error import HTTPError
from urllib.error import URLError
from urllib.parse import quote
from urllib.parse import unquote
from urllib.parse import urlparse
from urllib.request import Request
from urllib.request import urlopen

USER_AGENT = "DevResurgeShowcase/1.0 (+https://devresurge.com)"
MAX_BYTES = 1_500_000
TIMEOUT_SECONDS = 12

_GITHUB_HOSTS = {"github.com", "www.github.com"}
_RAW_HOSTS = {"raw.githubusercontent.com"}
_BLOB_RE = re.compile(
    r"^/(?P<owner>[^/]+)/(?P<repo>[^/]+)/(?:blob|raw)/(?P<ref>[^/]+)/(?P<path>.+)$",
)
_TREE_FILE_RE = re.compile(
    r"^/(?P<owner>[^/]+)/(?P<repo>[^/]+)/tree/(?P<ref>[^/]+)/(?P<path>.+)$",
)
_REPO_RE = re.compile(r"^/(?P<owner>[^/]+)/(?P<repo>[^/]+)/?$")


class GitHubFetchError(Exception):
    """User-facing fetch failure."""


@dataclass(frozen=True)
class GitHubRef:
    owner: str
    repo: str
    path: str
    ref: str = "main"

    @property
    def html_url(self) -> str:
        return f"https://github.com/{self.owner}/{self.repo}/blob/{self.ref}/{self.path}"

    @property
    def raw_url(self) -> str:
        path = "/".join(quote(part, safe="") for part in self.path.split("/"))
        return (
            f"https://raw.githubusercontent.com/{self.owner}/{self.repo}/"
            f"{quote(self.ref, safe='')}/{path}"
        )

    @property
    def api_url(self) -> str:
        path = "/".join(quote(part, safe="") for part in self.path.split("/"))
        return (
            f"https://api.github.com/repos/{self.owner}/{self.repo}/contents/"
            f"{path}?ref={quote(self.ref, safe='')}"
        )


def parse_github_url(url: str, *, default_ref: str = "main") -> GitHubRef:
    """Parse a github.com or raw.githubusercontent.com file URL into a ref."""
    raw = (url or "").strip()
    if not raw:
        msg = "Paste a GitHub file URL."
        raise GitHubFetchError(msg)

    parsed = urlparse(raw)
    host = (parsed.hostname or "").lower()
    path = unquote(parsed.path or "")

    if host in _RAW_HOSTS:
        parts = [p for p in path.split("/") if p]
        if len(parts) < 4:
            msg = "Raw GitHub URL must include owner, repo, branch, and file path."
            raise GitHubFetchError(msg)
        owner, repo, ref, *rest = parts
        return GitHubRef(owner=owner, repo=repo, ref=ref, path="/".join(rest))

    if host not in _GITHUB_HOSTS:
        msg = "Only github.com (or raw.githubusercontent.com) URLs are supported."
        raise GitHubFetchError(msg)

    for pattern in (_BLOB_RE, _TREE_FILE_RE):
        match = pattern.match(path)
        if match:
            return GitHubRef(
                owner=match.group("owner"),
                repo=match.group("repo").removesuffix(".git"),
                ref=match.group("ref"),
                path=match.group("path").rstrip("/"),
            )

    match = _REPO_RE.match(path)
    if match:
        msg = "Point to a specific file in the repo (blob URL), not the repo root."
        raise GitHubFetchError(msg)

    msg = "Unrecognized GitHub URL. Use a file link like github.com/org/repo/blob/main/path/file.md"
    raise GitHubFetchError(msg)


def is_excalidraw_embed(path: str) -> bool:
    """True for Excalidraw exports with embedded scene (PNG/SVG)."""
    name = path.rsplit("/", 1)[-1].lower()
    return name.endswith(".excalidraw.png") or name.endswith(".excalidraw.svg")


def is_excalidraw_source(path: str) -> bool:
    """True for editable Excalidraw JSON sources (not embedded exports)."""
    name = path.rsplit("/", 1)[-1].lower()
    if is_excalidraw_embed(path):
        return False
    return name.endswith(".excalidraw.json") or name.endswith(".excalidraw")


def detect_kind(path: str) -> str:
    """Map a file path to a ShowcaseKind value."""
    name = path.rsplit("/", 1)[-1].lower()
    if is_excalidraw_embed(path) or is_excalidraw_source(path):
        return "excalidraw"
    if name.endswith((".md", ".markdown", ".mdx")):
        return "markdown"
    if name.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")):
        return "image"
    if name.endswith((".txt", ".rst", ".adoc", ".org")):
        return "notes"
    return "notes"


def companion_preview_paths(path: str) -> list[str]:
    """Likely embedded Excalidraw PNG exports next to a JSON source file."""
    if not is_excalidraw_source(path):
        return []
    if "/" in path:
        directory, name = path.rsplit("/", 1)
        prefix = f"{directory}/"
    else:
        name = path
        prefix = ""
    stem = name
    for suffix in (".excalidraw.json", ".excalidraw"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    else:
        if "." in stem:
            stem = stem.rsplit(".", 1)[0]
    candidates = [
        f"{prefix}{stem}.excalidraw.png",
    ]
    # Preserve order, drop dupes.
    seen: set[str] = set()
    out: list[str] = []
    for item in candidates:
        if item not in seen and item != path:
            seen.add(item)
            out.append(item)
    return out


def _http_get(url: str, *, accept: str = "*/*") -> bytes:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": accept,
        },
        method="GET",
    )
    try:
        with urlopen(request, timeout=TIMEOUT_SECONDS) as response:  # noqa: S310
            length = response.headers.get("Content-Length")
            if length and length.isdigit() and int(length) > MAX_BYTES:
                msg = f"File is larger than {MAX_BYTES // 1024} KB."
                raise GitHubFetchError(msg)
            chunks: list[bytes] = []
            total = 0
            while True:
                chunk = response.read(64 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_BYTES:
                    msg = f"File is larger than {MAX_BYTES // 1024} KB."
                    raise GitHubFetchError(msg)
                chunks.append(chunk)
            return b"".join(chunks)
    except HTTPError as exc:
        if exc.code in {401, 403, 404}:
            msg = "File not found or repo is private. Only public GitHub files work."
            raise GitHubFetchError(msg) from exc
        msg = f"GitHub returned HTTP {exc.code}."
        raise GitHubFetchError(msg) from exc
    except URLError as exc:
        msg = "Could not reach GitHub. Try again in a moment."
        raise GitHubFetchError(msg) from exc
    except TimeoutError as exc:
        msg = "GitHub timed out. Try again."
        raise GitHubFetchError(msg) from exc


def fetch_bytes(ref: GitHubRef) -> bytes:
    """Download a public file as raw bytes (images, exports, etc.)."""
    return _http_get(ref.raw_url, accept="image/*, application/octet-stream, */*")


def resolve_excalidraw_ref(ref: GitHubRef) -> GitHubRef:
    """Prefer embedded .excalidraw.png over editable .excalidraw JSON sources."""
    if is_excalidraw_embed(ref.path):
        return ref
    if not is_excalidraw_source(ref.path):
        return ref
    for path in companion_preview_paths(ref.path):
        candidate = GitHubRef(owner=ref.owner, repo=ref.repo, ref=ref.ref, path=path)
        try:
            fetch_bytes(candidate)
        except GitHubFetchError:
            continue
        return candidate
    msg = (
        "Link the exported Excalidraw PNG (.excalidraw.png with embedded scene) "
        "instead of the .excalidraw source. In Excalidraw: File → Export → PNG, "
        "enable “Embed scene”, then commit e.g. designs/api.excalidraw.png."
    )
    raise GitHubFetchError(msg)


def fetch_text(ref: GitHubRef) -> str:
    """Download a public file as UTF-8 text."""
    data = _http_get(ref.raw_url, accept="text/plain, application/json, */*")
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        msg = "File is not valid UTF-8 text."
        raise GitHubFetchError(msg) from exc


def find_preview_url(ref: GitHubRef) -> str:
    """Return the first companion embedded PNG raw URL that exists, else empty."""
    if is_excalidraw_embed(ref.path):
        return ref.raw_url
    for path in companion_preview_paths(ref.path):
        candidate = GitHubRef(owner=ref.owner, repo=ref.repo, ref=ref.ref, path=path)
        try:
            fetch_bytes(candidate)
        except GitHubFetchError:
            continue
        return candidate.raw_url
    return ""
