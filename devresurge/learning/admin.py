from django.contrib import admin

from .models import LessonProgress


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "roadmap_slug", "lesson_slug", "status", "updated_at")
    list_filter = ("status", "roadmap_slug")
    search_fields = ("user__email", "roadmap_slug", "lesson_slug")
    raw_id_fields = ("user",)
    date_hierarchy = "updated_at"
