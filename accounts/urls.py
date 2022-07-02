from django.urls import path

from . import views

urlpatterns = [
    path("accounts/", views.ListCreateView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("accounts/newest/<int:num>/", views.ListNewestView.as_view()),
    path("accounts/<int:pk>/", views.UpdateAccountView.as_view()),
    path("accounts/<int:pk>/management/", views.UpdateActiveAccountView.as_view()),
]
