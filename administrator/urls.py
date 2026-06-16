from django.urls import path

from .views import (
    admin_dashboard,
    change_status,
    investor_chain
)


app_name = "administrator"



urlpatterns = [


    path(
        "",
        admin_dashboard,
        name="admin_dashboard"
    ),



    path(
        "change-status/<int:id>/",
        change_status,
        name="change_status"
    ),



    path(
        "chain/<int:id>/",
        investor_chain,
        name="investor_chain"
    ),


]