from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
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
            kwargs={"pk": self.object.pk},
        )


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = [
        "profile_picture",
        "profilename",
        "display_name",
        "bio",
        "location",
        "tags",
    ]
    template_name = "usercatalog/userprofile_form.html"

    def get_success_url(self):
        return reverse(
            "usercatalog:userprofile_detail",
            kwargs={"pk": self.object.pk},
        )


class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = "usercatalog/userprofile_detail.html"
    context_object_name = "userprofile"

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
        return context


class UserProfileListView(LoginRequiredMixin, ListView):
    model = UserProfile
    context_object_name = "userprofile_list"
    template_name = "usercatalog/userprofile_list.html"
    paginate_by = 10
