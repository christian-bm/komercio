from django.urls import path

from . import views

urlpatterns = [
    path("products/", views.ListCreateProductView.as_view()),
    path("products/<int:pk>/", views.RetrieveUpdateProductView.as_view()),
]
