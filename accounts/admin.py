from django.contrib import admin
from .models import Investor


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "investor_id",
        "full_name",
        "mobile",
        "email",
        "aadhar",
        "pan",
        "status",
    )

    search_fields = (
        "investor_id",
        "full_name",
        "mobile",
        "email",
        "aadhar",
        "pan",
    )

    list_filter = (
        "status",
        "city",
        "state",
    )

    ordering = ("-id",)