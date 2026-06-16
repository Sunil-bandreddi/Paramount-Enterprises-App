from django.db import models

from accounts.models import Investor

from django.contrib.auth.models import User



class AdminActivityLog(models.Model):


    ACTIONS = (

        ("ACTIVATE","ACTIVATE"),

        ("DEACTIVATE","DEACTIVATE"),

        ("VIEW","VIEW"),

        ("UPDATE","UPDATE"),

    )



    admin = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name="admin_actions"

    )


    investor = models.ForeignKey(

        Investor,

        on_delete=models.CASCADE,

        related_name="admin_logs"

    )


    action = models.CharField(

        max_length=20,

        choices=ACTIONS

    )


    description = models.TextField(

        blank=True

    )


    created = models.DateTimeField(

        auto_now_add=True

    )



    def __str__(self):

        return (

            self.admin.username

            +

            " - "

            +

            self.action

        )