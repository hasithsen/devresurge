from django.contrib import admin

from .models import Badge
from .models import Choice
from .models import Question
from .models import Quiz
from .models import QuizAttempt
from .models import UserBadge


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "topic", "pass_percent", "is_published", "order")
    list_filter = ("is_published", "topic")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "slug", "tagline")
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("prompt", "quiz", "order")
    list_filter = ("quiz",)
    search_fields = ("prompt",)
    inlines = [ChoiceInline]


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "category", "icon", "is_active", "order")
    list_filter = ("category", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "slug")


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "quiz", "percent", "passed", "created_at")
    list_filter = ("passed", "quiz")
    raw_id_fields = ("user", "quiz")
    date_hierarchy = "created_at"


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ("user", "badge", "earned_at")
    list_filter = ("badge",)
    raw_id_fields = ("user", "badge", "quiz_attempt")
    date_hierarchy = "earned_at"
