from django.contrib import admin

from habit_tracker.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "activity",
    )
    list_filter = ("owner",)
    search_fields = ("owner", "activity")
