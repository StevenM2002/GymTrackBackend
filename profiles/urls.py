from django.urls import path
from .views import SignUpAPI, Signer
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("signup/", SignUpAPI.as_view()),
    path("login/", obtain_auth_token),
    path("check/", Signer.as_view()),
]