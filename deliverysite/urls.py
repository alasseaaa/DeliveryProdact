"""
URL configuration for deliverysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from deliveryfood import views
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

SchemaView = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("category", views.CategoryViewSet)
router.register("profile", views.ProfileViewSet)
router.register("address", views.AddressViewSet)
router.register("order", views.OrderViewSet)
router.register("ordereditems", views.OrderedItemViewSet)

urlpatterns = [
    path("deliveryfood/", include("deliveryfood.urls")),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    path('products/', views.product_list, name='product_list'),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path('accounts/', include('allauth.urls')),
    path('swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('login/', views.user_login, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)