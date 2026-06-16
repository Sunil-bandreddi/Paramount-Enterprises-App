from django import forms
from django.contrib.auth.models import User

from .models import Investor


class RegisterForm(forms.Form):
    POSITION_CHOICES = (
        ("LEFT", "Left"),
        ("RIGHT", "Right"),
    )

    full_name = forms.CharField(max_length=100)
    dob = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    mobile = forms.CharField(max_length=10)
    email = forms.EmailField(required=False)
    sponsor = forms.CharField(required=False)
    position = forms.ChoiceField(choices=POSITION_CHOICES, required=False)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)
    aadhar = forms.CharField(max_length=12)
    pan = forms.CharField(max_length=10)
    account_no = forms.CharField(max_length=30)
    bank_name = forms.CharField(max_length=100)
    branch = forms.CharField(max_length=100)
    ifsc_code = forms.CharField(max_length=20)
    nominee = forms.CharField(max_length=100)
    nominee_relation = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    declaration = forms.BooleanField(required=True)

    def __init__(self, *args, is_first_registration=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_first_registration = is_first_registration

    def clean_mobile(self):
        mobile = "".join(filter(str.isdigit, self.cleaned_data["mobile"]))
        if len(mobile) != 10:
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        if Investor.objects.filter(mobile=mobile).exists() or User.objects.filter(username=mobile).exists():
            raise forms.ValidationError("This mobile number is already registered.")
        return mobile

    def clean_aadhar(self):
        aadhar = "".join(filter(str.isdigit, self.cleaned_data["aadhar"]))
        if len(aadhar) != 12:
            raise forms.ValidationError("Enter a valid 12-digit Aadhar number.")
        return aadhar

    def clean_pan(self):
        pan = self.cleaned_data["pan"].strip().upper()
        if len(pan) != 10:
            raise forms.ValidationError("Enter a valid 10-character PAN number.")
        return pan

    def clean_ifsc_code(self):
        return self.cleaned_data["ifsc_code"].strip().upper()

    def clean_sponsor(self):
        return self.cleaned_data.get("sponsor", "").strip().upper()

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password and confirm and password != confirm:
            self.add_error("confirm_password", "Password and confirm password do not match.")

        if not self.is_first_registration:
            if not cleaned_data.get("sponsor"):
                self.add_error("sponsor", "Sponsor ID is required.")
            if not cleaned_data.get("position"):
                self.add_error("position", "Placement side is required.")
        else:
            cleaned_data["sponsor"] = ""
            cleaned_data["position"] = ""

        return cleaned_data
