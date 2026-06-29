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


from .models import ContactEnquiry





@admin.register(ContactEnquiry)

class ContactEnquiryAdmin(admin.ModelAdmin):


    list_display = (

        "name",

        "email",

        "phone",

        "created_at",

        "is_read"

    )



    list_filter = (

        "is_read",

        "created_at"

    )



    search_fields = (

        "name",

        "email",

        "phone"

    )