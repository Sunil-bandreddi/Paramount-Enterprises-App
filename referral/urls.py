from django.urls import path

from .views import tree_api



app_name = "referral"



urlpatterns = [


    # Binary Tree JSON API

    path(

        'tree/',

        tree_api,

        name='tree_api'

    ),


]