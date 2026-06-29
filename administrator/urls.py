from django.urls import path

from administrator import views



app_name = "administrator"



urlpatterns = [



    # Admin Dashboard

    path(

        "",

        views.admin_dashboard,

        name="admin_dashboard"

    ),






    # Activate / Deactivate Investor

    path(

        "change-status/<int:id>/",

        views.change_status,

        name="change_status"

    ),






    # Investor Binary Chain

    path(

        "investor-chain/<int:id>/",

        views.investor_chain,

        name="investor_chain"

    ),






    # Edit Investor

    path(

        "investor-edit/<int:id>/",

        views.edit_investor,

        name="edit_investor"

    ),






    # Delete Investor

    path(

        "investor-delete/<int:id>/",

        views.delete_investor,

        name="delete_investor"

    ),






    # Download Reports

    # ?type=daily

    # ?type=weekly

    # ?type=overall


    path(

        "download-report/",

        views.download_report,

        name="download_report"

    ),


]