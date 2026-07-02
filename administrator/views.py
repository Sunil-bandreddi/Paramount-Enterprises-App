from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import (
    login_required,
    user_passes_test
)

from django.http import HttpResponse

from django.utils import timezone

from datetime import timedelta

from openpyxl import Workbook

from accounts.models import Investor,ContactEnquiry

from accounts.forms import InvestorEditForm
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


    users = Investor.objects.all().order_by(
        "-created"
    )



    investor_data = []



    for user in users:


        pair = get_pair_details(
            user
        )


        investor_data.append({

            "user": user,

            "pair": pair

        })



    # Contact Feedback Data

    enquiries = ContactEnquiry.objects.all().order_by(
        "-created_at"
    )



    context = {


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
            investor_data,



        # Send enquiries to dashboard template

        "enquiries":
            enquiries

    }



    return render(

        request,

        "admin_dashboard.html",

        context

    )






@login_required
@user_passes_test(admin_check)
def change_status(request, id):


    investor = get_object_or_404(

        Investor,

        id=id

    )



    if investor.status == "ACTIVE":


        investor.status = "INACTIVE"



    else:


        investor.status = "ACTIVE"




    investor.save()



    return redirect(

        "administrator:admin_dashboard"

    )









@login_required
@user_passes_test(admin_check)
def edit_investor(request,id):


    investor=get_object_or_404(
        Investor,
        id=id
    )



    if request.method=="POST":


        form=InvestorEditForm(
            request.POST
        )


        if form.is_valid():


            data=form.cleaned_data



            investor.full_name=data["full_name"]

            investor.dob=data["dob"]

            investor.mobile=data["mobile"]

            investor.email=data["email"]

            investor.address=data["address"]

            investor.city=data["city"]

            investor.state=data["state"]

            investor.aadhar=data["aadhar"]

            investor.pan=data["pan"]

            investor.account_no=data["account_no"]

            investor.bank_name=data["bank_name"]

            investor.branch=data["branch"]

            investor.ifsc_code=data["ifsc_code"]

            investor.nominee=data["nominee"]

            investor.nominee_relation=data["nominee_relation"]
            


            investor.save()



            return redirect(
                "administrator:admin_dashboard"
            )



    else:


        form=InvestorEditForm(

            initial={

                "full_name":investor.full_name,

                "dob":investor.dob,

                "mobile":investor.mobile,

                "email":investor.email,

                "address":investor.address,

                "city":investor.city,

                "state":investor.state,

                "aadhar":investor.aadhar,

                "pan":investor.pan,

                "account_no":investor.account_no,

                "bank_name":investor.bank_name,

                "branch":investor.branch,

                "ifsc_code":investor.ifsc_code,

                "nominee":investor.nominee,

                "nominee_relation":investor.nominee_relation,

            }

        )





    return render(

        request,

        "edit_investor.html",

        {

            "form":form,

            "investor":investor

        }

    )














@login_required
@user_passes_test(admin_check)
def investor_chain(request, id):


    investor = get_object_or_404(

        Investor,

        id=id

    )



    tree = build_chain(

        investor

    )




    return render(

        request,

        "investor_chain.html",

        {


            "tree": tree


        }

    )








@login_required
@user_passes_test(admin_check)
def download_report(request):



    report_type = request.GET.get(

        "type",

        "overall"

    )




    users = Investor.objects.all()






    today = timezone.now().date()





    if report_type == "daily":



        users = users.filter(

            created__date=today

        )





    elif report_type == "weekly":



        start_date = today - timedelta(days=7)



        users = users.filter(

            created__date__gte=start_date

        )







    workbook = Workbook()



    worksheet = workbook.active





    if report_type == "daily":


        worksheet.title = "Daily Report"



    elif report_type == "weekly":


        worksheet.title = "Weekly Report"



    else:


        worksheet.title = "Overall Report"







    worksheet.append([


        "Investor ID",

        "Name",

        "Mobile",

        "Email",

        "Status",

        "Left",

        "Right",

        "Pairs",

        "Created Date"


    ])







    for investor in users:



        pair = get_pair_details(

            investor

        )




        worksheet.append([


            investor.investor_id,


            investor.full_name,


            investor.mobile,


            investor.email,


            investor.status,


            pair["left"],


            pair["right"],


            pair["pairs"],


            investor.created.strftime(

                "%d-%m-%Y"

            )


        ])







    response = HttpResponse(


        content_type=

        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


    )





    filename = f"{report_type}_investor_report.xlsx"




    response[

        "Content-Disposition"

    ] = f"attachment; filename={filename}"





    workbook.save(response)




    return response