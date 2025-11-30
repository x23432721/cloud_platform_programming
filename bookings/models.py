from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

# Create your models here.

class Service(models.Model):
    SERVICE_TYPES = [
        ("oil_change", "Oil Change"),
        ("tyre_rotation", "Tyre Rotation"),
        ("full_service", "Full Service"),
        ("inspection", "Inspection"),
        ("car_wash", "Car Wash"),
    ]

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, choices=SERVICE_TYPES, unique=True)
    description = models.TextField(blank=True)
    base_duration_minutes = models.PositiveIntegerField(default=60)
    base_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ("sedan", "Sedan"),
        ("hatchback", "Hatchback"),
        ("suv", "SUV"),
        ("truck", "Truck"),
        ("other", "Other"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicles")
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES, default="sedan")
    license_plate = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="bookings")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="bookings")
    preferred_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    estimated_completion_time = models.DateTimeField(null=True, blank=True)
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    vehicle_photo_url = models.URLField(blank=True)

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username} - {self.service.name}"
