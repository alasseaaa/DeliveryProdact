from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from deliveryfood import views
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views

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
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('product/<int:id>/delete/', views.delete_product, name='delete_product'),
    path('product/<int:id>/edit/', views.edit_product, name='edit_product'),
    path('product/add/', views.add_product, name='add_product'),
    path('', views.product_list, name='product_list'),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path('accounts/', include('allauth.urls')),
    path('swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('login/', auth_views.LoginView.as_view(template_name='deliveryfood/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('orders/', views.orders_view, name='orders_view'),
    # path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)