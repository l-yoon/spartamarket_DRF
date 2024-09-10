from django.urls import path
from . import views

urlpatterns = [
    path("",views.SignupView.as_view()),
    path("login/",views.LoginView.as_view()),
    path("logout/",views.LogoutView.as_view()),
    path("<str:username>/",views.ProfileView.as_view()),
]
