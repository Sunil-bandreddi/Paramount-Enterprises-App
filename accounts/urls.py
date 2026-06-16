from django.urls import path
from .views import register_api
from accounts.views import (
    login_view,
    register,
    logout_view
)



urlpatterns = [


    path(
        'login/',
        login_view,
        name='login'
    ),



    # path(
    #     'register/',
    #     register,
    #     name='register'
    # ),
    path('api/register/',register_api, name='register_api'),



    path(
        'logout/',
        logout_view,
        name='logout'
    ),

]