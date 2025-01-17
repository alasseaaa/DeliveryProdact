"""
Модуль представлений для приложения доставки еды.
"""
import time
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.core.cache import cache
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from rest_framework.filters import SearchFilter
from .models import Product, Category, Profile
from .models import Address, Order, OrderedItem
from .serializers import ProductSerializer, CategorySerializer, ProfileSerializer
from .serializers import AddressSerializer, OrderSerializer, OrderedItemSerializer

def product_list(request):
    products = Product.objects.all()
    return render(request, 'deliveryfood/product_list.html', {'products': products})

def product_detail(request, id):
    """
    Отображает информацию о продукте.

    Эта функция получает информацию о продукте по его id 
    и отображает ее на странице product_detail.html.
    """
    start_time = time.time()
    cache_key = f"product_{id}"
    product = cache.get(cache_key)
    
    if product is None:
        # Получаем продукт по id
        product = get_object_or_404(Product, id=id)
        cache.set(cache_key, product, timeout=60*15)  # Кэш на 15 минут
    
    end_time = time.time()
    print(f"Время выполнения с кэшем: {end_time - start_time:.4f} секунд")
    
    return render(
        request,
        "deliveryfood/product_detail.html",  # Убедитесь, что путь к шаблону правильный
        {
            "product": product,
        },
    )

class ProductFilter(django_filters.FilterSet):
    """
    Фильтр для модели Product.

    Позволяет фильтровать товары по категории, описанию, 
    а также минимальной и максимальной цене.
    """
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr="gt")
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr="lt")

    class Meta:
        """
        Метаданные для фильтра.
        
        model:  Указывает, к какой модели применяется фильтр.
        fields:  Указывает, какие поля модели должны быть отфильтрованы.
        """
        model = Product
        fields = ["category", "description", "min_price", "max_price"]

class ProductPriceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product, 
    используемый для изменения цены.

    Ограничивает цену, чтобы она была не меньше нуля.
    """
    class Meta:
        """
        Метаданные для сериализатора.
        
        model:  Указывает, к какой модели применяется сериализатор.
        fields:  Указывает, какие поля модели должны быть сериализованы.
        """
        model = Product
        fields = ['price']

    def validate_price(self, value):
        """
        Проверяет, что цена не меньше нуля.
        """
        if value <0:
            raise serializers.ValidationError("Цена не может быть меньше нуля.")
        return value

class ProductViewSet(viewsets.ModelViewSet):
    """
    API-представление для модели Product.

    Предоставляет CRUD-операции, 
    а также действия для статистики,
    изменения цены и сортировки по ней.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name", "description", "category__category_name"]
    filterset_class = ProductFilter

    @action(methods=["GET"], detail=False)
    def statistics(self, request):
        """
        Сводная статистика.
        """
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
        """
        Изменяет цену товара.
        """
        product = self.get_object()
        serializer = ProductPriceSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "цена изменена"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        """
        Возвращает сериализатор, который нужно использовать для действия "change_price".
        """
        if self.action == 'change_price':
            return ProductPriceSerializer
        return super().get_serializer_class()

    @action(methods=['GET'], detail=False)
    def sorted_by_price(self, request):
        """
        Сортирует товары по цене(возростание).
        """
        sorted_products = self.queryset.order_by('price')
        serializer = self.get_serializer(sorted_products, many=True)
        return Response(serializer.data)


    @action(methods=['GET'], detail=False)
    def milk_not_gte_100(self, request):
        """
        Выборка товаров по цене меньше 100 и из категорий 
        Молочные продукты или Хлебобулочные изделия.
        """
        selected_products = Product.objects.filter(
            ~Q(price__gte=100) &
            (Q(category__category_name="Молочные продукты") |
            Q(category__category_name="Хлебобулочные изделия"))
        )
        serializer1 = ProductSerializer(selected_products, many=True)
        return Response ({"Молочка и выпечка стоимостью < 100" : serializer1.data,})

    @action(methods=['GET'], detail=False)
    def vtoroy_zapros(self, request):
        """
        Выборка товаров из категорий 
        (Молочные продукты и по цене больше 200) или
        (Хлебобулочные изделия и по цене меньше 100).
        """
        selected_products = Product.objects.filter(
            (Q(category__category_name="Молочные продукты")&~Q(price__lte=200))
            | (Q(category__category_name="Хлебобулочные изделия") &~Q(price__gte=100))
        )
        serializer2 = ProductSerializer(selected_products, many=True)
        return Response ({"Выбранные товары" : serializer2.data,})



class CategoryViewSet(viewsets.ModelViewSet):
    """
    API-представление для модели Category.

    Предоставляет CRUD-операции.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["category_name"]

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API-представление для модели Profile.

    Предоставляет CRUD-операции.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [SearchFilter]
    search_fields = ['full_name']

class AddressViewSet(viewsets.ModelViewSet):
    """
    API-представление для модели Address.

    Предоставляет CRUD-операции.
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [SearchFilter]
    search_fields = ['address']

class OrderFilter(django_filters.FilterSet):
    """
    Фильтр для модели OrderedItem.

    Позволяет фильтровать по дате заказа.
    """
    class Meta:
        """
        Метаданные для фильтра.
        
        model:  Указывает, к какой модели применяется фильтр.
        fields:  Указывает, какие поля модели должны быть отфильтрованы.
        """
        model = Order
        fields = ['order_date']

class OrderViewSet(viewsets.ModelViewSet):
    """
    API-представление для модели Order.

    Предоставляет CRUD-операции.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter
    filter_backends = [SearchFilter, DjangoFilterBackend]

class OrderedItemFilter(django_filters.FilterSet):
    """
    Фильтр для модели OrderedItem.

    Позволяет фильтровать товары по наименованию.
    """
    class Meta:
        """
        Метаданные для фильтра.
        
        model:  Указывает, к какой модели применяется фильтр.
        fields:  Указывает, какие поля модели должны быть отфильтрованы.
        """
        model = OrderedItem
        fields = ['product']

class OrderedItemViewSet(viewsets.ModelViewSet):
    """
    API-представление для модели OrderedItem.

    Предоставляет CRUD-операции.
    """
    queryset = OrderedItem.objects.all()
    serializer_class = OrderedItemSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = OrderedItemFilter

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session.set_expiry(5)  # Устанавливаем срок действия сеанса в 600 секунд
                return redirect('deliveryfood:product_list')
            else:
                return HttpResponse('Профиль не активен.')
        else:
            return HttpResponse('Неверные логин или пароль.')
    else:
        return render(request, 'admin/login.html')

def index(request):
    """
    index
    """
    return HttpResponse("Hello, world. You're at the index.")
