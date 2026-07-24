from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import RegisterForm
from .models import Investor

from accounts.utils import generate_investor_id, is_admin

from referral.models import ReferralTree

from referral.services import (
    validate_sponsor,
    calculate_level,
    sync_weekly_activity,
    check_aadhar_allowed
)


def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def projects(request):
    return render(request, "projects.html")


def gallery(request):
    return render(request, "gallery.html")


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

        messages.success(request, "Your enquiry has been submitted successfully.")

        return redirect("contact")

    return render(request, "contact.html")


def terms(request):
    return render(request, "terms.html")


# ============================
# LOGIN
# ============================

def login_view(request):

    if request.method == "POST":

        # This field historically held "Aadhar Number", but now also
        # needs to accept a plain username (admin logins, and the 3
        # seed/company accounts which log in via username, not Aadhar).
        identifier = request.POST.get("username")
        password = request.POST.get("password")

        user = None

        # 1) Try it as a literal Django username first - this covers
        #    admin/staff logins and the seed investor accounts (#1-3).
        user = authenticate(request, username=identifier, password=password)

        # 2) If that failed, `identifier` may be an Aadhar number.
        #    From investor #4 onward, when an Aadhar is REUSED, the
        #    real login username falls back to the investor_id (since
        #    the Aadhar is already taken by the earlier position) - so
        #    look up every investor position for this Aadhar and try
        #    each one's real username with the given password.
        if user is None:

            matching_positions = Investor.objects.filter(
                aadhar=identifier
            ).select_related("user")

            for position in matching_positions:

                candidate = authenticate(
                    request,
                    username=position.user.username,
                    password=password
                )

                if candidate is not None:
                    user = candidate
                    break

        if user is not None:

            login(request, user)

            # ADMIN LOGIN
            if user.is_staff:
                return redirect("administrator:admin_dashboard")

            # INVESTOR LOGIN
            if hasattr(user, "investor"):
                return redirect("dashboard")

        return render(
            request,
            "login.html",
            {"error": "Invalid Aadhar number / username or password"}
        )

    return render(request, "login.html")


@login_required
@user_passes_test(is_admin)
def register(request):

    investor_count = Investor.objects.count()

    # Investor #1 (root/CEO) has no sponsor at all.
    is_first_registration = investor_count == 0

    # Investors #1, #2, #3 (CEO + 2 employees) are the company's own
    # seed accounts: they log in with an admin-chosen username instead
    # of their Aadhar, and are exempt from the Aadhar re-use rule.
    is_seed_registration = investor_count < 3

    if request.method == "POST":

        form = RegisterForm(
            request.POST,
            is_first_registration=is_first_registration,
            is_seed_registration=is_seed_registration
        )

        if form.is_valid():

            aadhar = form.cleaned_data["aadhar"]

            # ============================
            # AADHAR RE-USE ELIGIBILITY
            # (seed registrations #1-3 are exempt)
            # ============================

            if not is_seed_registration:

                allowed, aadhar_error = check_aadhar_allowed(aadhar)

                if not allowed:
                    return render(
                        request,
                        "register.html",
                        {
                            "form": form,
                            "error": aadhar_error,
                            "is_first_registration": is_first_registration,
                            "is_seed_registration": is_seed_registration
                        }
                    )

            # ============================
            # SPONSOR VALIDATION
            # (skipped entirely for the very first / root registration)
            # ============================

            if is_first_registration:
                sponsor, error = None, None
            else:
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
                        "error": error,
                        "is_first_registration": is_first_registration,
                        "is_seed_registration": is_seed_registration
                    }
                )

            investor_id = generate_investor_id()

            # ============================
            # CREATE USER
            #
            # Default (ID #4+, first time this Aadhar is used):
            #   login username = the Aadhar number itself, as before.
            #
            # Seed accounts (#1-3):
            #   login username = the admin-entered text in the
            #   "Login Username" field.
            #
            # Reused Aadhar (ID #4+, 2nd/3rd/4th use of the same
            # Aadhar): the Aadhar is already taken as a username by
            # the earlier position, so this one silently falls back
            # to the investor_id as its login username instead - no
            # extra field, this is invisible to the person filling
            # the form.
            # ============================

            if is_seed_registration:
                login_username = form.cleaned_data["username"]
            else:
                aadhar_already_used = Investor.objects.filter(aadhar=aadhar).exists()
                login_username = investor_id if aadhar_already_used else aadhar

            user = User.objects.create_user(
                username=login_username,
                password=form.cleaned_data["password"],
                email=form.cleaned_data.get("email")
            )

            # ============================
            # CREATE INVESTOR
            # ============================

            investor = Investor.objects.create(
                user=user,
                investor_id=investor_id,
                sponsor=sponsor,
                placement=form.cleaned_data.get("position"),
                full_name=form.cleaned_data["full_name"],
                dob=form.cleaned_data["dob"],
                mobile=form.cleaned_data["mobile"],
                email=form.cleaned_data.get("email"),
                aadhar=aadhar,
                pan=form.cleaned_data.get("pan"),
                account_no=form.cleaned_data["account_no"],
                bank_name=form.cleaned_data["bank_name"],
                branch=form.cleaned_data["branch"],
                ifsc_code=form.cleaned_data["ifsc_code"],
                address=form.cleaned_data["address"],
                city=form.cleaned_data["city"],
                state=form.cleaned_data["state"],
                nominee=form.cleaned_data["nominee"],
                nominee_relation=form.cleaned_data["nominee_relation"],
                status="ACTIVE"
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

                sync_weekly_activity(investor)

            return render(request, "reg_success.html", {"investor": investor})

    else:

        form = RegisterForm(
            is_first_registration=is_first_registration,
            is_seed_registration=is_seed_registration
        )

    return render(
        request,
        "register.html",
        {
            "form": form,
            "is_first_registration": is_first_registration,
            "is_seed_registration": is_seed_registration
        }
    )


def logout_view(request):
    logout(request)
    return redirect("login")