from __future__ import annotations

from factory import Faker
from factory import SubFactory
from factory.django import DjangoModelFactory

from devresurge.profiles.models import Profile
from devresurge.profiles.models import ProjectLink
from devresurge.profiles.models import ShowcaseItem
from devresurge.profiles.models import ShowcaseKind
from devresurge.profiles.models import SocialLink
from devresurge.users.tests.factories import UserFactory


class ProfileFactory(DjangoModelFactory[Profile]):
    user = SubFactory(UserFactory)
    handle = Faker("user_name")
    display_name = Faker("name")
    headline = Faker("sentence", nb_words=6)
    bio = Faker("paragraph")
    location = Faker("city")
    tech_stack = "python, django, postgres"
    is_public = True

    class Meta:
        model = Profile
        django_get_or_create = ("user",)


class ProjectLinkFactory(DjangoModelFactory[ProjectLink]):
    profile = SubFactory(ProfileFactory)
    title = Faker("catch_phrase")
    description = Faker("sentence")
    url = Faker("url")
    repo_url = Faker("url")
    tech_stack = "python, fastapi"

    class Meta:
        model = ProjectLink


class ShowcaseItemFactory(DjangoModelFactory[ShowcaseItem]):
    profile = SubFactory(ProfileFactory)
    title = Faker("catch_phrase")
    summary = Faker("sentence")
    kind = ShowcaseKind.MARKDOWN
    github_url = "https://github.com/acme/lab/blob/main/notes/readme.md"
    github_owner = "acme"
    github_repo = "lab"
    github_path = "notes/readme.md"
    github_ref = "main"
    tags = "notes, github"
    content_cache = "# Hello\n\nNotes from the lab."
    is_published = True

    class Meta:
        model = ShowcaseItem

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        if not kwargs.get("slug") and kwargs.get("title"):
            from slugify import slugify

            kwargs["slug"] = slugify(kwargs["title"])[:80] or "showcase"
        return super()._create(model_class, *args, **kwargs)


class SocialLinkFactory(DjangoModelFactory[SocialLink]):
    profile = SubFactory(ProfileFactory)
    platform = "github"
    label = "github"
    url = Faker("url")

    class Meta:
        model = SocialLink
