from django.shortcuts import render,redirect

from django.contrib.auth.decorators import login_required,user_passes_test


from accounts.models import Investor

from referral.models import ReferralTree



def admin_check(user):

    return (
        user.is_staff
        or
        user.is_superuser
    )





@login_required
@user_passes_test(admin_check)
def admin_dashboard(request):


    users=Investor.objects.all().order_by(
        "-created"
    )



    context={


        "total_users":
        users.count(),



        "active_users":
        users.filter(
            status="ACTIVE"
        ).count(),



        "pending_users":
        users.filter(
            status="PENDING"
        ).count(),



        "inactive_users":
        users.filter(
            status="INACTIVE"
        ).count(),



        "users":users


    }



    return render(

        request,

        "admin_dashboard.html",

        context

    )






@login_required
@user_passes_test(admin_check)
def change_status(request,id):


    investor=Investor.objects.get(
        id=id
    )



    if investor.status=="ACTIVE":


        investor.status="INACTIVE"


    else:


        investor.status="ACTIVE"



    investor.save()



    return redirect(
    "administrator:admin_dashboard"
)







@login_required
@user_passes_test(admin_check)
def investor_chain(request,id):


    investor=Investor.objects.get(
        id=id
    )


    levels={}



    def count_level(user,level):


        if level>6:

            return



        children=ReferralTree.objects.filter(

            sponsor=user

        )


        levels[level]=levels.get(level,0)+children.count()



        for child in children:


            count_level(

                child.investor,

                level+1

            )



    count_level(
        investor,
        1
    )



    return render(

        request,

        "investor_chain.html",

        {

        "investor":investor,

        "levels":levels

        }

    )