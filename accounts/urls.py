from django.urls import path
from .views import register_api
from django.contrib.auth import views as auth_views
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



    path(
        'register/',
        register,
        name='register'
    ),
    path('api/register/',register_api, name='register_api'),



    path(
        'logout/',
        logout_view,
        name='logout'
    ),

     path(
        'forgot-password/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset.html'
        ),
        name='password_reset'
    ),


    path(
        'forgot-password/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),


    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),


    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),


]