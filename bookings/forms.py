from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Vehicle, Booking


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ["make", "model", "year", "vehicle_type", "license_plate"]


class BookingForm(forms.ModelForm):
    vehicle_photo = forms.ImageField(required=False, label="Vehicle Photo (optional)")

    class Meta:
        model = Booking
        fields = ["vehicle", "service", "preferred_date", "notes"]
        widgets = {
            "preferred_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["vehicle"].queryset = user.vehicles.all()
