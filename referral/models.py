from django.db import models

from accounts.models import Investor



class ReferralTree(models.Model):


    POSITION_CHOICES = (

        ("LEFT","LEFT"),

        ("RIGHT","RIGHT")

    )



    investor = models.OneToOneField(

        Investor,

        on_delete=models.CASCADE,

        related_name="referral_node"

    )



    sponsor = models.ForeignKey(

        Investor,

        related_name="referral_children",

        null=True,

        blank=True,

        on_delete=models.CASCADE

    )



    position = models.CharField(

        max_length=10,

        choices=POSITION_CHOICES,

        null=True,

        blank=True

    )



    level = models.PositiveIntegerField(

        default=0

    )



    created = models.DateTimeField(

        auto_now_add=True

    )



    updated = models.DateTimeField(

        auto_now=True

    )



    class Meta:


        constraints = [

            models.UniqueConstraint(

                fields=[

                    "sponsor",

                    "position"

                ],

                name="unique_binary_position"

            )

        ]



    def __str__(self):

        return self.investor.investor_id



    # -----------------------------
    # Left Child
    # -----------------------------

    def left_child(self):

        return ReferralTree.objects.filter(

            sponsor=self.investor,

            position="LEFT"

        ).first()



    # -----------------------------
    # Right Child
    # -----------------------------

    def right_child(self):

        return ReferralTree.objects.filter(

            sponsor=self.investor,

            position="RIGHT"

        ).first()



    # -----------------------------
    # Complete Team Count
    # -----------------------------

    def team_count(self):


        count = 0


        children = ReferralTree.objects.filter(

            sponsor=self.investor

        )


        for child in children:

            count += 1

            count += child.team_count()


        return count





class WeeklyActivity(models.Model):


    STATUS_CHOICES = (

        ("CURRENT","CURRENT"),

        ("PREVIOUS","PREVIOUS")

    )



    investor = models.ForeignKey(

        Investor,

        on_delete=models.CASCADE,

        related_name="weekly_activity"

    )



    week_number = models.PositiveIntegerField()



    monday = models.DateField()



    saturday = models.DateField()



    total_referrals = models.PositiveIntegerField(default=0)

    # ADD THIS:
    level = models.PositiveIntegerField(default=0)



    status=models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default="CURRENT"

    )



    created=models.DateTimeField(

        auto_now_add=True

    )



    updated=models.DateTimeField(

        auto_now=True

    )



    class Meta:


        constraints=[

            models.UniqueConstraint(

                fields=[

                    "investor",

                    "week_number"

                ],

                name="unique_week_activity"

            )

        ]



    def __str__(self):

        return (

            self.investor.investor_id

            +

            " Week "

            +

            str(self.week_number)

        )