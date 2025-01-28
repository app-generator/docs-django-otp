from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.otp_login, name="otp_login"),
    path("logout/", views.logout_view, name="logout"),
    path("validate/<int:code>/", views.validate_otp, name="validate_otp"),
]
