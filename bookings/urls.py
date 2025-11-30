from django.urls import path
from .views import (
    register_view,
    CustomLoginView,
    CustomLogoutView,
    dashboard_view,
    ServiceListView,
    vehicle_create_view,
    booking_create_view,
    booking_success_view,
    booking_detail_view,
    vehicle_list_view,  
    vehicle_edit_view,      
    vehicle_delete_view,
)

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("services/", ServiceListView.as_view(), name="service_list"),
    path("vehicles/", vehicle_list_view, name="vehicle_list"),
    path("vehicle/create/", vehicle_create_view, name="vehicle_create"),
    path("vehicle/<int:pk>/edit/", vehicle_edit_view, name="vehicle_edit"),
    path("vehicle/<int:pk>/delete/", vehicle_delete_view, name="vehicle_delete"),
    path("booking/create/", booking_create_view, name="booking_create"),
    path("booking/<int:pk>/success/", booking_success_view, name="booking_success"),
    path("booking/<int:pk>/", booking_detail_view, name="booking_detail"),
    path("register/", register_view, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
