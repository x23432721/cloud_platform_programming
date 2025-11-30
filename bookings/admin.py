from django.contrib import admin
from .models import Booking, Vehicle, Service
# Register your models here.

admin.site.register(Booking)
admin.site.register(Vehicle)    
admin.site.register(Service)