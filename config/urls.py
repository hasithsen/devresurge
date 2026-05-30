from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include
from django.urls import path
from django.views import defaults as default_views
from django.views.decorators.cache import cache_control
from django.views.generic import TemplateView

from devresurge.profiles.views import home_view


@cache_control(max_age=60 * 60 * 24, public=True)
def robots_txt(_request):
    body = "User-agent: *\nDisallow: /me/\nDisallow: /accounts/\nDisallow: /admin/\nAllow: /\n"
    return HttpResponse(body, content_type="text/plain")


urlpatterns = [
    path("", home_view, name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path("robots.txt", robots_txt, name="robots"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("devresurge.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Profiles app (public + private CRUD)
    path("", include("devresurge.profiles.urls", namespace="profiles")),
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
            *urlpatterns,
        ]
