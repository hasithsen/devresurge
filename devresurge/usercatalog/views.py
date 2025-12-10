from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView

from .forms import UserProfileForm
from .models import DevresurgeUser
from .models import UserProfile


class UserProfileCreateView(LoginRequiredMixin, CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "usercatalog/userprofile_form.html"

    def form_valid(self, form):
        # ensure there is a DevresurgeUser for the logged-in User and link it
        dev_user, _ = DevresurgeUser.objects.get_or_create(user=self.request.user)
        form.instance.devresurge_user = dev_user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "usercatalog:userprofile_detail",
            kwargs={"profilename": self.object.profilename},
        )


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = [
        "profilename",
        "display_name",
        "location",
        "tags",
        "linkedin_url",
    ]
    template_name = "usercatalog/userprofile_form.html"
    slug_url_kwarg = "profilename"
    slug_field = "profilename"

    def get_success_url(self):
        return reverse(
            "usercatalog:userprofile_detail",
            kwargs={"profilename": self.object.profilename},
        )


class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = UserProfile
    success_url = reverse_lazy(
        "usercatalog:userprofile_list",
    )


class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = "usercatalog/userprofile_detail.html"
    context_object_name = "userprofile"
    slug_url_kwarg = "profilename"
    slug_field = "profilename"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object

        tags_list = []
        tags_attr = getattr(profile, "tags", None)

        if tags_attr is None:
            tags_list = []
        else:
            # If tags is a RelatedManager (ManyToMany) use .all()
            all_callable = getattr(tags_attr, "all", None)
            try:
                if callable(all_callable):
                    iterable = tags_attr.all()
                    # Convert tag objects to display strings
                    tags_list = [str(t).strip() for t in iterable if str(t).strip()]
                else:
                    # Fallback: assume a comma-separated string
                    raw = str(tags_attr)
                    tags_list = [t.strip() for t in raw.split(",") if t.strip()]
            except Exception:
                raw = str(tags_attr)
                tags_list = [t.strip() for t in raw.split(",") if t.strip()]

        context["tags_list"] = tags_list

        job_titles_list = []
        job_titles_attr = getattr(profile, "job_titles", None)

        if job_titles_attr is None:
            job_titles_list = []
        else:
            # If job_titles is a RelatedManager (ManyToMany) use .all()
            all_callable = getattr(job_titles_attr, "all", None)
            try:
                if callable(all_callable):
                    iterable = job_titles_attr.all()
                    # Convert tag objects to display strings
                    job_titles_list = [
                        str(t).strip() for t in iterable if str(t).strip()
                    ]
                else:
                    # Fallback: assume a comma-separated string
                    raw = str(job_titles_attr)
                    job_titles_list = [t.strip() for t in raw.split(",") if t.strip()]
            except Exception:
                raw = str(job_titles_attr)
                job_titles_list = [t.strip() for t in raw.split(",") if t.strip()]

        context["job_titles_list"] = job_titles_list

        return context


class UserProfileListView(ListView):
    model = UserProfile
    context_object_name = "userprofile_list"
    template_name = "usercatalog/userprofile_list.html"
    paginate_by = 10

    def get_queryset(self):
        # select_related to avoid extra queries for username
        qs = super().get_queryset().select_related("devresurge_user__user")
        # prepare tags_list on each profile (split comma-separated tags)
        for p in qs:
            raw = getattr(p, "tags", "") or ""
            p.tags_list = [t.strip() for t in raw.split(",") if t.strip()]
        return qs
