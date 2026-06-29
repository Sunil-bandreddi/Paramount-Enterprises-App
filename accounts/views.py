from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import RegisterForm
from .models import Investor

from accounts.utils import generate_investor_id


from referral.models import ReferralTree

from referral.services import (
    check_aadhar_allowed,
    validate_sponsor,
    calculate_level
)



def home(request):

    return render(
        request,
        "home.html"
    )




def about(request):

    return render(
        request,
        "about.html"
    )




def projects(request):

    return render(
        request,
        "projects.html"
    )




def gallery(request):

    return render(
        request,
        "gallery.html"
    )



from .models import ContactEnquiry
from django.contrib import messages

def contact(request):

    if request.method == "POST":

        name = request.POST.get("name")

        email = request.POST.get("email")

        phone = request.POST.get("phone")

        message = request.POST.get("message")



        ContactEnquiry.objects.create(

            name=name,

            email=email,

            phone=phone,

            message=message

        )


        messages.success(
            request,
            "Your enquiry has been submitted successfully."
        )


        return redirect("contact")



    return render(
        request,
        "contact.html"
    )



def terms(request):

    return render(
        request,
        "terms.html"
    )

# ============================
# LOGIN
# ============================

# ============================
# LOGIN
# ============================

def login_view(request):

    if request.method == "POST":


        # Aadhar Number entered by user

        aadhar = request.POST.get(
            "username"
        )


        password = request.POST.get(
            "password"
        )



        # Authenticate using Aadhar

        user = authenticate(

            request,

            username=aadhar,

            password=password

        )



        if user is not None:


            login(

                request,

                user

            )



            # ADMIN LOGIN

            if user.is_staff :


                return redirect(
                    "administrator:admin_dashboard"
                )



            # INVESTOR LOGIN

            if hasattr(
                user,
                "investor"
            ):


                return redirect(
                    "dashboard"
                )




        return render(

            request,

            "login.html",

            {

                "error":
                "Invalid Aadhar number or password"

            }

        )



    return render(

        request,

        "login.html"

    )







# ============================
# REGISTER
# ============================

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)


        if form.is_valid():

            aadhar = form.cleaned_data["aadhar"]



            # ============================
            # AADHAR VALIDATION
            # ============================

            if not check_aadhar_allowed(aadhar):

                return render(
                    request,
                    "register.html",
                    {
                        "form": form,
                        "error":
                        "Aadhar already used and 6 level chain not completed"
                    }
                )



            # ============================
            # SPONSOR VALIDATION
            # ============================

            sponsor, error = validate_sponsor(

                form.cleaned_data.get("sponsor"),

                form.cleaned_data.get("position")

            )


            if error:

                return render(
                    request,
                    "register.html",
                    {
                        "form": form,
                        "error": error
                    }
                )



            # ============================
            # CREATE DJANGO USER
            # USERNAME = AADHAR NUMBER
            # ============================


            aadhar = form.cleaned_data["aadhar"]


            user = User.objects.create_user(

                username=aadhar,

                password=form.cleaned_data["password"],

                email=form.cleaned_data["email"]

            )


            # Optional email save

            user.email = form.cleaned_data.get("email")

            user.save()



            # ============================
            # CREATE INVESTOR PROFILE
            # ============================


            investor = Investor.objects.create(

                user=user,


                investor_id=generate_investor_id(),


                full_name=form.cleaned_data["full_name"],


                dob=form.cleaned_data["dob"],


                mobile=form.cleaned_data["mobile"],


                email=form.cleaned_data["email"],


                aadhar=aadhar,


                pan=form.cleaned_data["pan"],


                account_no=form.cleaned_data["account_no"],


                bank_name=form.cleaned_data["bank_name"],


                branch=form.cleaned_data["branch"],


                ifsc_code=form.cleaned_data["ifsc_code"],


                address=form.cleaned_data["address"],


                city=form.cleaned_data["city"],


                state=form.cleaned_data["state"],


                nominee=form.cleaned_data["nominee"],


                nominee_relation=form.cleaned_data["nominee_relation"],


                status="PENDING"

            )



            # ============================
            # CREATE REFERRAL TREE
            # ============================


            if sponsor:


                ReferralTree.objects.create(

                    investor=investor,

                    sponsor=sponsor,

                    position=form.cleaned_data["position"],

                    level=calculate_level(sponsor)

                )



            return render(
                request,
                "reg_success.html",
                {
                    "investor": investor
                }
            )



    else:

        form = RegisterForm()



    return render(

        request,

        "register.html",

        {
            "form":form
        }

    )







from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.models import User

from .models import Investor, InvestorSequence

from referral.models import ReferralTree
from referral.services import calculate_level



@api_view(["POST"])
def register_api(request):

    data = request.data


    try:


        # Duplicate mobile check

        if Investor.objects.filter(
            mobile=data.get("mobileNo")
        ).exists():

            return Response(
                {
                    "status":"error",
                    "message":"Mobile already registered"
                },
                status=400
            )



        # Sponsor validation

        sponsor = None


        sponsor_id = data.get("sponsorId")


        if sponsor_id:


            sponsor = Investor.objects.filter(
                investor_id=sponsor_id
            ).first()


            if not sponsor:

                return Response(
                    {
                        "status":"error",
                        "message":"Invalid Sponsor ID"
                    },
                    status=400
                )



        # Position validation

        position = data.get(
            "placement"
        ).upper()



        if sponsor:


            exists = ReferralTree.objects.filter(

                sponsor=sponsor,

                position=position

            ).exists()



            if exists:

                return Response(
                    {
                        "status":"error",
                        "message":
                        f"{position} position already filled"
                    },
                    status=400
                )



        # Generate PME ID

        sequence,created = InvestorSequence.objects.get_or_create(
            id=1
        )


        sequence.current_number += 1

        sequence.save()



        investor_id = (
            f"PME{sequence.current_number:06d}"
        )



        # Create Login User


        user = User.objects.create_user(

            username=data.get("emailId"),

            email=data.get("emailId"),

            password=data.get("password")

        )



        # Create Investor


        investor = Investor.objects.create(

            user=user,

            investor_id=investor_id,

            sponsor=sponsor,

            placement=position,

            full_name=data.get("fullName"),

            dob=data.get("dob"),

            mobile=data.get("mobileNo"),

            email=data.get("emailId"),

            aadhar=data.get("adharNo"),

            pan=data.get("panCardNo"),

            account_no=data.get("accountNo"),

            bank_name=data.get("bankName"),

            branch=data.get("branch"),

            ifsc_code=data.get("ifscCode"),

            address=data.get("address"),

            city=data.get("city"),

            state=data.get("state"),

            nominee=data.get("nominee"),

            nominee_relation=data.get("relationship")

        )



        # CREATE BINARY TREE NODE  ⭐ IMPORTANT


        if sponsor:


            ReferralTree.objects.create(

                investor=investor,

                sponsor=sponsor,

                position=position,

                level=calculate_level(sponsor)

            )



        return Response(
            {

                "status":"success",

                "message":
                "Registration Completed",

                "investor_id":
                investor.investor_id

            }
        )



    except Exception as e:


        return Response(

            {
                "status":"error",
                "message":str(e)
            },

            status=400

        )



def logout_view(request):

    logout(request)

    return redirect("login")