from django.contrib import admin
from .models import ReferralTree, WeeklyActivity


@admin.register(ReferralTree)
class ReferralTreeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "investor",
        "sponsor",
        "position",
        "level",
        "created",
    )

    search_fields = (
        "investor__full_name",
        "investor__investor_id",
        "sponsor__full_name",
        "sponsor__investor_id",
    )

    list_filter = (
        "position",
        "level",
    )

    ordering = ("-id",)


@admin.register(WeeklyActivity)
class WeeklyActivityAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "investor",
        "week_number",
        "monday",
        "saturday",
        "total_referrals",
        "status",
        "created",
    )

    search_fields = (
        "investor__full_name",
        "investor__investor_id",
    )

    list_filter = (
        "status",
        "week_number",
    )

    ordering = ("-id",)