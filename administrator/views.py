from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth.decorators import login_required,user_passes_test

from django.http import HttpResponse

from openpyxl import Workbook

from accounts.models import Investor

from referral.models import WeeklyActivity

from .utils import (
    get_pair_details,
    build_chain
)




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



    investor_data=[]


    for user in users:


        pair=get_pair_details(
            user
        )


        investor_data.append({

            "user":user,

            "pair":pair

        })





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



        "investors":
        investor_data


    }


    return render(

        request,

        "admin_dashboard.html",

        context

    )









@login_required
@user_passes_test(admin_check)
def change_status(request,id):


    investor=get_object_or_404(

        Investor,

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


    investor=get_object_or_404(

        Investor,

        id=id

    )


    tree=build_chain(

        investor

    )


    return render(

        request,

        "investor_chain.html",

        {

        "tree":tree

        }

    )











@login_required
@user_passes_test(admin_check)
def download_report(request):


    wb=Workbook()


    ws=wb.active

    ws.title="Weekly Report"



    ws.append([

        "Investor ID",

        "Name",

        "Status",

        "Left",

        "Right",

        "Pairs"

    ])




    for investor in Investor.objects.all():


        pair=get_pair_details(
            investor
        )



        ws.append([

            investor.investor_id,

            investor.full_name,

            investor.status,

            pair["left"],

            pair["right"],

            pair["pairs"]

        ])




    response=HttpResponse(

        content_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )



    response[
        "Content-Disposition"
    ] = "attachment; filename=weekly_report.xlsx"



    wb.save(response)



    return response