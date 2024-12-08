from django.http import HttpResponse
import django_filters
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.db.models import Count, Q
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, serializers, status
from .models import Product, Category, Profile, Address, Order, OrderedItem
from .serializers import ProductSerializer, CategorySerializer, ProfileSerializer, AddressSerializer, OrderSerializer, OrderedItemSerializer

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        model = Product
        fields = ["category", "description", "min_price", "max_price"]

class ProductPriceSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ['price']
            
        def validate_price(self, value):
            if value <0:
                raise serializers.ValidationError("Цена не может быть меньше нуля.")
            return value 

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name", "description", "category__category_name"]
    filterset_class = ProductFilter

    @action(methods=["GET"], detail=False)
    def statistics(self, request):
       
        all_count = self.get_queryset().count()
        category_count = (
            self.get_queryset().values("category__category_name").annotate(count=Count("id"))
        )

        return Response(
            {
                "Всего товаров": all_count,
                "Статистика по категориям": category_count,
            }
        )


    @action(methods=['POST', 'GET'], detail=True)
    def change_price(self, request, pk=None):

        product = self.get_object()
        serializer = ProductPriceSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "цена изменена"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_serializer_class(self):

        if self.action == 'change_price':
            return ProductPriceSerializer
        return super().get_serializer_class()
   
    @action(methods=['GET'], detail=False)
    def sorted_by_price(self, request):
        sorted_products = self.queryset.order_by('price')
        serializer = self.get_serializer(sorted_products, many=True)
        return Response(serializer.data)


    @action(methods=['GET'], detail=False)
    def milk_not_gte_100(self, request):
        selected_products = Product.objects.filter(
            ~Q(price__gte=100) &
            (Q(category__category_name="Молочные продукты") |
            Q(category__category_name="Хлебобулочные изделия"))
        )
        serializer1 = ProductSerializer(selected_products, many=True)
        return Response ({"Молочка и выпечка стоимостью < 100" : serializer1.data,})

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