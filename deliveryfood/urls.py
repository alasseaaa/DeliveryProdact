from django.conf import settings
from django.urls import include, path
from rest_framework import routers
from . import views

# # app_name = "deliveryfood"



urlpatterns = [
    path("", views.index, name="index"),
    path('__debug__/', include('debug_toolbar.urls')),
]

# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns