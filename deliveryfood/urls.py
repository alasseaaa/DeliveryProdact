from django.urls import include, path
from rest_framework import routers
from . import views

# # app_name = "deliveryfood"



urlpatterns = [
    path("", views.index, name="index"),
]
