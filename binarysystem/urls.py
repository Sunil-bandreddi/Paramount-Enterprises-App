"""
URL configuration for binarysystem project.
"""

from django.contrib import admin

from django.urls import (
    path,
    include
)

from accounts.views import home,contact,projects,about,terms,gallery

from django.conf import settings

from django.conf.urls.static import static



urlpatterns = [


    # Django Built-in Admin

    path(

        'admin/',

        admin.site.urls

    ),



    # User Registration and Login

    path(

        "",

        include(
            'accounts.urls'
        )

    ),
    path(
        "",
        home,
        name="home"
    ),


    path(
        "about/",
        about,
        name="about"
    ),


    path(
        "projects/",
        projects,
        name="projects"
    ),


    path(
        "gallery/",
        gallery,
        name="gallery"
    ),


    path(
        "contact/",
        contact,
        name="contact"
    ),
    path(
        "terms/",
        terms,
        name="terms"
    ),



    # Investor Dashboard

    path(

        'dashboard/',

        include(
            'dashboard.urls'
        )

    ),



    # Referral Binary Tree

    path(

        'referral/',

        include(
            'referral.urls'
        )

    ),



    # Separate PME Admin Dashboard

    path('admin-panel/',include('administrator.urls',namespace='administrator')
),


]



# Development Media Handling

if settings.DEBUG:


    urlpatterns += static(

        settings.MEDIA_URL,

        document_root=settings.MEDIA_ROOT

    )


    urlpatterns += static(

        settings.STATIC_URL,

        document_root=settings.STATIC_ROOT

    )