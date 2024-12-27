"""
Модуль для настройки административной панели Django для приложения deliveryfood.
"""
import time
from django.contrib import admin
from django.core.cache import cache
# from django.db import connection
from import_export.admin import ExportActionModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import Category, Product, Profile, Address, Order, OrderedItem
from .export import AddressResource, CategoryResource
from .export import OrderResource, OrderedItemResource
from .export import ProductResource, ProfileResource

CACHE_TIMEOUT = 60 * 15  # 15 минут


@admin.register(Category)
class CategoryAdmin(SimpleHistoryAdmin, ExportActionModelAdmin):
    """
    Админ-класс для управления категориями.
    """
    list_display = [
        'category_name',
    ]

    search_fields = (
            "category_name",
        )
    resource_class = CategoryResource

@admin.register(Product)
class ProductAdmin(SimpleHistoryAdmin, ExportActionModelAdmin):
    """
    Админ-класс для управления продуктами.
    """
    list_display = [
        'name',
        'category',
        'description',
        'price',
    ]
    # поиск
    search_fields = (
        "name",
        "price",
        "description",
    )
    # фильтрация
    list_filter = ["name"]
    # изменение полей
    list_editable = ["price"]
    list_display_links = ["name"]
    resource_class = ProductResource

    def get_queryset(self, request):
        """
        Переопределяем метод для получения QuerySet, добавляем кэширование.
        """
        start_time = time.time()
        cache_key = 'product_admin_queryset'  # уникальный ключ для кэша
        cached_data = cache.get(cache_key)

        if cached_data is None:
            print("Запрос к базе данных, т.к. кэша нет")

            queryset = super().get_queryset(request)

            # Создаем копию queryset в виде списка, т.к. QuerySet нельзя закэшировать
            cached_data = list(queryset)

            cache.set(cache_key, cached_data, timeout=CACHE_TIMEOUT)  # Кэш на 15 минут
        else:
            print("Данные получены из кэша")

        #  Возвращаем queryset из закэшированных данных

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Время выполнения запроса: {execution_time:.4f} секунд")


        # Создаем QuerySet из кэшированных данных
        return Product.objects.filter(pk__in=[item.pk for item in cached_data])

@admin.register(Profile)
class ProfileAdmin(SimpleHistoryAdmin, ExportActionModelAdmin):
    """
    Админ-класс для управления профилями пользователей.
    """
    list_display = [
        'full_name',
        'email',
        'phone',
    ]

    search_fields = (
        'full_name',
        'email',
    )

    list_filter = ["full_name"]
    resource_class = ProfileResource

@admin.register(Address)
class AddressAdmin(SimpleHistoryAdmin, ExportActionModelAdmin):
    """
    Админ-класс для управления адресами пользователей.
    """
    list_display = [
        'user',
        'address',
    ]
    search_fields = (
        'address',
        'user__full_name',
    )
    resource_class = AddressResource

class OrderInline(admin.TabularInline):
    """
    Встраиваемый класс для управления заказанными товарами в заказе.
    """
    model = OrderedItem
    raw_id_fields=['product',]

@admin.register(Order)
class OrderAdmin(SimpleHistoryAdmin, ExportActionModelAdmin):
    """
    Админ-класс для управления заказами.
    """
    list_display = ['id', 'user', 'user_addresses', 'order_date',]
    readonly_fields = ['order_date']
    raw_id_fields=['user', 'user_addresses']
    inlines = [OrderInline]
    search_fields = (
        'id',
        'user__full_name',
        'user__email'
    )
    resource_class = OrderResource

@admin.register(OrderedItem)
class OrderedItemAdmin(SimpleHistoryAdmin, ExportActionModelAdmin):
    """
    Админ-класс для управления заказанными товарами.
    """
    list_display = [
        'order',
        'product',
        'product_quantity',
       'get_total_item_price',
    ]
    resource_class = OrderedItemResource

    def get_total_item_price(self, obj):
        """
        получение цены
        """
        return obj.product.price * obj.product_quantity

    get_total_item_price.short_description = 'Итоговая цена'
