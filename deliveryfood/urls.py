from django.urls import path

from . import views

# # app_name = "deliveryfood"

urlpatterns = [
    path("", views.index, name="index"),
]