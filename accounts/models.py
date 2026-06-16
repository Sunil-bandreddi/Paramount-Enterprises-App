from django.db import models
from django.contrib.auth.models import User



class Investor(models.Model):


    STATUS=(

        ("PENDING","PENDING"),

        ("ACTIVE","ACTIVE"),

        ("INACTIVE","INACTIVE")

    )


    user=models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    sponsor = models.ForeignKey(
       'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="team"
    )


    placement = models.CharField(
        max_length=10,
        choices=[
            ("LEFT","LEFT"),
            ("RIGHT","RIGHT")
        ],
        null=True,
        blank=True
    )


    investor_id=models.CharField(
        max_length=20,
        unique=True
    )



    full_name=models.CharField(
        max_length=100
    )



    dob=models.DateField()



    mobile=models.CharField(
        max_length=10,
        unique=True
    )



    email=models.EmailField(
        blank=True,
        null=True
    )



    aadhar=models.CharField(
        max_length=12
    )



    pan=models.CharField(
        max_length=10
    )
    

    # Banking Details Added

    account_no=models.CharField(
        max_length=30
    )


    bank_name=models.CharField(
        max_length=100
    )


    branch=models.CharField(
        max_length=100
    )


    ifsc_code=models.CharField(
        max_length=20
    )


    address=models.TextField()



    city=models.CharField(
        max_length=50
    )



    state=models.CharField(
        max_length=50
    )



    nominee=models.CharField(
        max_length=100
    )



    nominee_relation=models.CharField(
        max_length=50
    )



    status=models.CharField(
        max_length=20,
        choices=STATUS,
        default="PENDING"
    )



    created=models.DateTimeField(
        auto_now_add=True
    )



    def __str__(self):

        return self.investor_id




class InvestorSequence(models.Model):


    current_number=models.IntegerField(
        default=0
    )