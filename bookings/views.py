from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView

from datetime import timedelta
from decimal import Decimal

from .forms import UserRegisterForm, VehicleForm, BookingForm
from .models import Service, Booking, Vehicle
from .aws_utils import upload_file_to_s3, send_booking_to_sqs

from autoservice_pro import ServiceEstimator, calculate_price

# create your views here.



def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserRegisterForm()
    return render(request, "registration/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = AuthenticationForm


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")



@login_required
def dashboard_view(request):
    bookings = Booking.objects.filter(user=request.user).select_related("vehicle", "service").order_by("-created_at")
    services = Service.objects.all()
    return render(
        request,
        "bookings/dashboard.html",
        {"bookings": bookings, "services": services},
    )



class ServiceListView(ListView):
    model = Service
    template_name = "bookings/service_list.html"
    context_object_name = "services"



@login_required
def vehicle_create_view(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            return redirect("vehicle_list")
    else:
        form = VehicleForm()
    return render(request, "bookings/vehicle_create.html", {"form": form})

@login_required
def booking_create_view(request):
    if request.method == "POST":
        form = BookingForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user

            photo = form.cleaned_data.get("vehicle_photo")
            if photo:
                url = upload_file_to_s3(photo, key_prefix=f"user_{request.user.id}/bookings")
                booking.vehicle_photo_url = url

            service = booking.service
            estimator = ServiceEstimator()
            estimated_minutes = estimator.estimate_time(
                service_type=service.code,
                workload="medium",
            )

            vehicle_type = booking.vehicle.vehicle_type
            estimated_price = calculate_price(
                service_type=service.code,
                vehicle_type=vehicle_type,
                add_ons=[],
            )

            # now = timezone.now()
            booked_date = booking.preferred_date
            booking.estimated_completion_time = booked_date + timedelta(minutes=estimated_minutes)
            booking.estimated_price = Decimal(str(estimated_price))

            booking.save()

            message_id = send_booking_to_sqs(booking)
            # print("DEBUG send_booking_to_sqs returned:", message_id)

            return redirect("booking_success", pk=booking.id)
    else:
        form = BookingForm(user=request.user)

    return render(request, "bookings/booking_create.html", {"form": form})


@login_required
def booking_success_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, "bookings/booking_success.html", {"booking": booking})


@login_required
def booking_detail_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, "bookings/booking_detail.html", {"booking": booking})

@login_required
def vehicle_list_view(request):
    vehicles = Vehicle.objects.filter(owner=request.user).order_by("make", "model")
    return render(request, "bookings/vehicle_list.html", {"vehicles": vehicles})

def vehicle_edit_view(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)

    if request.method == "POST":
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect("vehicle_list")
    else:
        form = VehicleForm(instance=vehicle)

    return render(request, "bookings/vehicle_edit.html", {"form": form, "vehicle": vehicle})

@login_required
def vehicle_delete_view(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)

    if request.method == "POST":
        vehicle.delete()
        return redirect("vehicle_list")

    return render(request, "bookings/vehicle_confirm_delete.html", {"vehicle": vehicle})

from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    next_page = "login"  