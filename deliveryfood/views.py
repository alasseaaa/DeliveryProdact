from django.http import HttpResponse
import django_filters
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers
from .models import Product, Category, Profile, Address, Order, OrderedItem
from .serializers import ProductSerializer, CategorySerializer, ProfileSerializer, AddressSerializer, OrderSerializer, OrderedItemSerializer

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Product
        fields = ["category", "description", "min_price", "max_price"]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name", "description", "category"]
    filterset_class = ProductFilter

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["category_name"]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [SearchFilter]
    search_fields = ['full_name']

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [SearchFilter]
    search_fields = ['аddress', "user"]


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['order_date']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]


class OrderedItemFilter(django_filters.FilterSet):
    class Meta:
        model = OrderedItem
        fields = ['product']

class OrderedItemViewSet(viewsets.ModelViewSet):
    queryset = OrderedItem.objects.all()
    serializer_class = OrderedItemSerializer
    filterset_class = OrderedItemFilter

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")