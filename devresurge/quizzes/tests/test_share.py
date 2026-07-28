from __future__ import annotations

from urllib.parse import parse_qs
from urllib.parse import urlparse

from devresurge.quizzes.share import build_badge_share_links


def test_build_badge_share_links_platforms():
    links = build_badge_share_links(
        page_url="https://devresurge.com/quizzes/badges/quiz_python/",
        title="Python Pulse",
        description="Passed the Python fundamentals quiz.",
        earned=True,
    )
    assert "I earned" in links["caption"]
    assert "Python Pulse" in links["caption"]

    linkedin = urlparse(links["linkedin"])
    assert linkedin.netloc == "www.linkedin.com"
    assert parse_qs(linkedin.query)["url"] == [
        "https://devresurge.com/quizzes/badges/quiz_python/",
    ]

    x = urlparse(links["x"])
    assert x.netloc == "twitter.com"
    assert "url" in parse_qs(x.query)
    assert "text" in parse_qs(x.query)

    assert links["reddit"].startswith("https://www.reddit.com/submit?")
    assert links["whatsapp"].startswith("https://wa.me/?")
    assert "Python Pulse" in parse_qs(urlparse(links["whatsapp"]).query)["text"][0]
    assert links["email"].startswith("mailto:?")
    assert links["page_url"].endswith("/quizzes/badges/quiz_python/")
