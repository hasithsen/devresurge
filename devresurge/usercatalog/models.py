from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

from devresurge.users.models import User


class DevresurgeUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_hiring = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}"


class UserProfile(models.Model):
    # Relation to DevresurgeUser
    devresurge_user = models.OneToOneField(
        "DevresurgeUser",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    profilename = models.CharField(
        max_length=30,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_]+$",
                message="Profile name can only contain alphanumeric characters and underscores",
                code="invalid_profilename",
            ),
        ],
        verbose_name="Profile handle",
    )
    display_name = models.CharField(max_length=255, default="")
    bio = models.TextField(
        blank=True,
        default="",
        verbose_name="About",
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Lives in",
    )
    # Tags
    tags = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Skills",
        help_text="Enter skills as a comma-separated list (ex: linux, bash, kubernetes).",
    )
    # Profile picture
    profile_picture = models.ImageField(
        upload_to="userprofile_pics/",
        blank=True,
        null=True,
    )
    linkedin_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="LinkedIn",
        help_text="Link to your LinkedIn profile",
    )
    job_titles = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Seeking job titles",
        help_text="Enter job titles as a comma-separated list (ex: DevOps Engineer, Site Reliability Engineer, Cloud Engineer).",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        hiring = False
        if getattr(self, "devresurge_user", None):
            hiring = bool(self.devresurge_user.is_hiring)
        return f"{self.profilename} - {'hiring' if hiring else ''}"

    def get_absolute_url(self):
        return reverse("userprofiles:detail", kwargs={"profilename": self.profilename})


class SocialLink(models.Model):
    user_profile = models.ForeignKey(
        "UserProfile",
        on_delete=models.CASCADE,
    )
    # Foreign Key used because social_link can only have one UserProfile, but UserProfiles can have multiple social_links.
    # UserProfile as a string rather than object because it hasn't been declared yet in file.
    platform_name = models.CharField(max_length=50)
    profile_url = models.URLField()
    link_index = models.IntegerField(default=0, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user_profile} - {self.platform_name} - {self.link_index}"

    def get_absolute_url(self):
        return reverse("userprofiles:detail", kwargs={"pk": self.user.pk})


class UserProfileView(models.Model):
    profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="views",
        db_index=True,
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    referrer = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"View for {self.profile.profilename} at {self.timestamp}"


class SocialLinkClick(models.Model):
    social_link = models.ForeignKey(
        "SocialLink", on_delete=models.CASCADE, related_name="clicks"
    )
    userprofile_view = models.ForeignKey(
        "UserProfileView", on_delete=models.CASCADE, related_name="social_link_clicks"
    )
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Click on {self.social_link.platform_name} for {self.userprofile_view.profile.profilename} at {self.timestamp}"
