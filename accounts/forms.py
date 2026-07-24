from django import forms
from django.contrib.auth.models import User

from .models import Investor
from referral.models import ReferralTree



class RegisterForm(forms.Form):


    POSITION_CHOICES = (

        ("LEFT", "Left"),
        ("RIGHT", "Right"),

    )



    full_name = forms.CharField(
        max_length=100
    )



    dob = forms.DateField(

        input_formats=["%Y-%m-%d"],

        widget=forms.DateInput(
            attrs={
                "type": "date"
            }
        )

    )



    mobile = forms.CharField(
        max_length=10
    )



    email = forms.EmailField(
        required=False
    )



    sponsor = forms.CharField(
        required=False
    )



    position = forms.ChoiceField(
        choices=POSITION_CHOICES,
        required=False
    )



    # Only used for the first 3 (seed / company) registrations -
    # CEO + 2 employees log in with a plain username instead of their
    # Aadhar number, since their Aadhar values are not treated as
    # unique login credentials for these seed accounts.
    username = forms.CharField(
        max_length=150,
        required=False
    )



    address = forms.CharField(
        widget=forms.Textarea
    )



    city = forms.CharField(
        max_length=50
    )



    state = forms.CharField(
        max_length=50
    )



    aadhar = forms.CharField(
        max_length=12
    )



    pan = forms.CharField(
        max_length=10,
        required=False
    )



    account_no = forms.CharField(
        max_length=30
    )



    bank_name = forms.CharField(
        max_length=100
    )



    branch = forms.CharField(
        max_length=100
    )



    ifsc_code = forms.CharField(
        max_length=20
    )



    nominee = forms.CharField(
        max_length=100
    )



    nominee_relation = forms.CharField(
        max_length=50
    )



    password = forms.CharField(
        widget=forms.PasswordInput
    )



    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )



    declaration = forms.BooleanField(
        required=True
    )





    def __init__(
        self,
        *args,
        is_first_registration=False,
        is_seed_registration=False,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.is_first_registration = is_first_registration
        self.is_seed_registration = is_seed_registration





    # ============================
    # MOBILE DUPLICATE CHECK
    # ============================


    def clean_mobile(self):

        mobile = "".join(
            filter(str.isdigit, self.cleaned_data.get("mobile", ""))
        )

        if len(mobile) != 10:
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")

        # Seed accounts (#1-3 / CEO + 2 employees) are exempt - their
        # mobile numbers can repeat, since these are internal company
        # accounts, not separate real customers.
        if self.is_seed_registration:
            return mobile

        if Investor.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError("This mobile number is already registered.")

        if User.objects.filter(username=mobile).exists():
            raise forms.ValidationError("This mobile number is already registered.")

        return mobile






    # ============================
    # AADHAR DUPLICATE CHECK
    # ============================


    def clean_aadhar(self):

        aadhar = "".join(
            filter(str.isdigit, self.cleaned_data.get("aadhar", ""))
        )

        if len(aadhar) != 12:
            raise forms.ValidationError("Enter a valid 12-digit Aadhar number.")

        # NOTE: Aadhar uniqueness is intentionally NOT enforced here.
        # From investor #4 onward, the same Aadhar CAN be reused (up to
        # 3 times, gated on 6-level downline completion) - that check
        # is done in accounts.views.register() via
        # referral.services.check_aadhar_allowed().

        return aadhar






    # ============================
    # PAN VALIDATION
    # ============================


    def clean_pan(self):


        pan = self.cleaned_data.get(
            "pan",
            ""
        ).strip().upper()



        if pan and len(pan) != 10:


            raise forms.ValidationError(

                "Enter a valid PAN number."

            )



        return pan






    def clean_ifsc_code(self):

        return self.cleaned_data.get(
            "ifsc_code",
            ""
        ).strip().upper()






    def clean_sponsor(self):

        return self.cleaned_data.get(
            "sponsor",
            ""
        ).strip().upper()






    # ============================
    # PASSWORD + POSITION CHECK
    # ============================


    def clean(self):


        cleaned_data = super().clean()



        password = cleaned_data.get(
            "password"
        )


        confirm = cleaned_data.get(
            "confirm_password"
        )



        if password and confirm:


            if password != confirm:


                self.add_error(

                    "confirm_password",

                    "Password and confirm password do not match."

                )





        sponsor_id = cleaned_data.get(
            "sponsor"
        )


        position = cleaned_data.get(
            "position"
        )



        if not self.is_first_registration:



            if not sponsor_id:


                self.add_error(

                    "sponsor",

                    "Sponsor ID is required."

                )



            if not position:


                self.add_error(

                    "position",

                    "Placement side is required."

                )



            # ============================
            # POSITION ALREADY FILLED
            # ============================


            if sponsor_id and position:


                sponsor = Investor.objects.filter(

                    investor_id=sponsor_id

                ).first()



                if sponsor:



                    exists = ReferralTree.objects.filter(

                        sponsor=sponsor,

                        position=position

                    ).exists()



                    if exists:


                        self.add_error(

                            "position",

                            f"{position} position is already filled for this sponsor."

                        )




        else:


            cleaned_data["sponsor"] = None

            cleaned_data["position"] = None


        # ============================
        # USERNAME CHECK (first 3 / seed registrations only)
        # ============================

        # ============================
        # USERNAME CHECK (first 3 / seed registrations only)
        # ============================

        if self.is_seed_registration:

            username = (cleaned_data.get("username", "") or "").strip()

            if not username:
                self.add_error("username", "Username is required for this seed (company) account.")
            elif User.objects.filter(username=username).exists():
                self.add_error("username", "This username is already taken.")
            else:
                cleaned_data["username"] = username

        return cleaned_data


      







# ==================================================
# INVESTOR EDIT FORM
# ==================================================


class InvestorEditForm(forms.Form):


    full_name = forms.CharField(
        max_length=100
    )


    dob = forms.DateField(

        input_formats=["%Y-%m-%d"],

        widget=forms.DateInput(
            attrs={
                "type":"date"
            }
        )

    )


    mobile = forms.CharField(
        max_length=10
    )


    email = forms.EmailField(
        required=False
    )


    address = forms.CharField(
        widget=forms.Textarea
    )


    city = forms.CharField(
        max_length=50
    )


    state = forms.CharField(
        max_length=50
    )


    aadhar = forms.CharField(
        max_length=12
    )


    pan = forms.CharField(
        max_length=10,
        required=False
    )


    account_no = forms.CharField(
        max_length=30
    )


    bank_name = forms.CharField(
        max_length=100
    )


    branch = forms.CharField(
        max_length=100
    )


    ifsc_code = forms.CharField(
        max_length=20
    )


    nominee = forms.CharField(
        max_length=100
    )


    nominee_relation = forms.CharField(
        max_length=50
    )