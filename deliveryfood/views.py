"""
Модуль представлений для приложения доставки еды.
"""
from django import template
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
from .models import BestSeller, Product, Category, ProductForm, ProductReview, Profile, StoreFact, StoreReview, UserRegistrationForm
from .models import Address, Order, OrderedItem
from .serializers import ProductSerializer, CategorySerializer, ProfileSerializer
from .serializers import AddressSerializer, OrderSerializer, OrderedItemSerializer
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum

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
        product = get_object_or_404(Product, id=id)
        cache.set(cache_key, product, timeout=60*15)
    
    reviews = ProductReview.objects.filter(product=product)

    end_time = time.time()
    print(f"Время выполнения с кэшем: {end_time - start_time:.4f} секунд")
    
    return render(
        request,
        "deliveryfood/product_detail.html",
        {
            "product": product,
            'reviews': reviews
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

    def exclude_expensive(self, request):
        """
        Исключает товары с ценой больше 100.
        """
        products = Product.objects.exclude(price__gt=100)
        serializer = ProductSerializer(products, many=True)
        return Response({"products_excluded_expensive": serializer.data})

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
                return redirect('product_list')
            else:
                return HttpResponse('Профиль не активен.')
        else:
            return HttpResponse('Неверные логин или пароль.')
    else:
        return render(request, 'deliveryfood/login.html')

def index(request):
    """
    Главная страница, отображающая список продуктов.
    """
    products = Product.objects.all()
    return render(request, 'deliveryfood/base.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Сохраняем успешное сообщение в сессии
            request.session['success_message'] = 'Продукт добавлен успешно!'
            return redirect('product_list')
        else:
            # Сохраняем данные формы в сессии
            request.session['form_data'] = request.POST
            request.session['form_errors'] = form.errors
            return redirect('add_product')
    else:
        # Восстанавливаем данные формы из сессии, если они есть
        form_data = request.session.get('form_data', None)
        form_errors = request.session.get('form_errors', None)
        if form_data:
            form = ProductForm(form_data)
        else:
            form = ProductForm()
        # Очищаем данные сессии после использования
        request.session['form_data'] = None
        request.session['form_errors'] = None

        # Получаем успешное сообщение из сессии и очищаем его
        success_message = request.session.pop('success_message', None)

    return render(request, 'deliveryfood/add_product.html', {'form': form, 'form_errors': form_errors, 'success_message': success_message})


@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()
    return redirect('product_list')


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            # Сохраняем успешное сообщение в сессии
            request.session['success_message'] = 'Продукт обновлен успешно!'
            return redirect('product_list')
        else:
            # Сохраняем данные формы в сессии
            request.session['form_data'] = request.POST
            request.session['form_errors'] = form.errors
            return redirect('edit_product', pk=pk)
    else:
        # Восстанавливаем данные формы из сессии, если они есть
        form_data = request.session.get('form_data', None)
        form_errors = request.session.get('form_errors', None)
        if form_data:
            form = ProductForm(form_data, instance=product)
        else:
            form = ProductForm(instance=product)
        # Очищаем данные сессии после использования
        request.session['form_data'] = None
        request.session['form_errors'] = None

        # Получаем успешное сообщение из сессии и очищаем его
        success_message = request.session.pop('success_message', None)

    return render(request, 'deliveryfood/edit_product.html', {'form': form, 'form_errors': form_errors, 'success_message': success_message})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'deliveryfood/register.html', {'form': form})

def product_list(request):
    search_query = request.GET.get('search', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category = request.GET.get('category')
    ordering = request.GET.get('ordering', 'price')
    exclude_expensive = request.GET.get('exclude_expensive')

    products = Product.objects.all()

    if exclude_expensive:
        products = Product.objects.exclude_expensive() 

    if search_query:
        products = products.filter(name__icontains=search_query)
    
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
        
    if category:
        products = products.filter(category__id=category)

    products = products.order_by(ordering)
    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except Exception as e:
        page_obj = paginator.get_page(1)
        print(f"Pagination error: {e}")
    
    categories = Category.objects.all()
    
    filtered_product_count = products.count()
    
    store_facts = StoreFact.objects.all()
    
    best_sellers = BestSeller.objects.all().order_by('-sales_count')
    store_reviews = StoreReview.objects.all().order_by('-created_at')
    
    total_product_price = products.aggregate(total_price=Sum('price'))['total_price']
    
    products_data = products.values('id', 'name', 'price', 'category__category_name')
    product_prices = products.values_list('price', flat=True)

    return render(
        request, 
        'deliveryfood/product_list.html', 
        {
            'page_obj': page_obj,
            'search': search_query,
            'min_price': min_price,
            'max_price': max_price,
            'categories': categories,
            'selected_category': category,
            'exclude_expensive': exclude_expensive,
            'filtered_product_count': filtered_product_count,
            'best_sellers': best_sellers,
            'store_reviews': store_reviews,
            'store_facts': store_facts,
            'total_product_price': total_product_price,
            'products_data': products_data,
            'product_prices': product_prices
        }
    )


@login_required
def orders_view(request):
    """
    Страница с заказами и пользователями.
    """
    orders = Order.objects.all()
    customer_names = Profile.objects.values_list('full_name', flat=True)

    return render(request, 'deliveryfood/orders.html', {
        'orders': orders,
        'customer_names': customer_names
    })
