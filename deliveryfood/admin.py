"""
Модуль для настройки административной панели Django для приложения deliveryfood.
"""
import time
from django.contrib import admin
from django.http import FileResponse
from django.utils.safestring import mark_safe
from import_export import resources
from django.core.cache import cache
# from django.db import connection
from import_export.admin import ExportActionModelAdmin
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from simple_history.admin import SimpleHistoryAdmin
from .models import Category, Product, Profile, Address, Order, OrderedItem
from .export import AddressResource, CategoryResource
from .export import OrderResource, OrderedItemResource
from .export import ProductResource, ProfileResource

CACHE_TIMEOUT = 60 * 15  # 15 минут
pdfmetrics.registerFont(TTFont('OpenSans', 'fonts/OpenSans-Regular.ttf'))

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
        "get_short_description",
        'price',
        'file',
        'url',
    ]
    # поиск
    search_fields = (
        "name",
        "price",
        "description",
        "image_visible",
    )
    # фильтрация
    list_filter = ["name"]
    # изменение полей
    list_editable = ["price"]
    list_display_links = ["name"]
    resource_class = ProductResource


    @admin.display(description='Краткое описание')  # Использование @admin.display
    def get_short_description(self, obj):
        """
        Возвращает краткое описание объекта.
        Описание объекта, сокращенное до первых пятидесяти символов.
        """
        return (
            obj.description[:50] + "..."
            if len(obj.description) > 50
            else obj.description
        )
    
    def generate_pdf(self, request, queryset):
        """
        Действие для генерации PDF-документа с информацией о выбранных товарах.
        """
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        y_position = 10.5 * inch  # Начальная позиция по оси Y

        # Устанавливаем шрифт для кириллицы
        p.setFont("OpenSans", 12)

        for product in queryset:
            textobject = p.beginText()
            textobject.setTextOrigin(inch, y_position)  # Устанавливаем позицию текста
            
            # Добавляем текст с использованием кириллицы
            textobject.textLine(f"Name: {product.name}")
            textobject.textLine(f"Price, RUB: {product.price}")
            textobject.textLine(f"Category: {product.category}")
            textobject.textLine("-" * 30)

            p.drawText(textobject)
            y_position -= 1.5 * inch  # Корректируем позицию для следующей записи
            
            if y_position <= inch:  # Проверяем не ушли ли мы вниз страницы
                p.showPage()  # Начинаем новую страницу
                y_position = 10.5 * inch  # Возвращаем позицию к началу новой страницы
                p.setFont("OpenSans", 12)  # Устанавливаем шрифт снова на новой странице

        p.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='products.pdf')

    generate_pdf.short_description = "Сгенерировать PDF"
    actions = ['generate_pdf']

    # def get_queryset(self, request):
    #     """
    #     Переопределяем метод для получения QuerySet, добавляем кэширование.
    #     """
    #     start_time = time.time()
    #     cache_key = 'product_admin_queryset'  # уникальный ключ для кэша
    #     cached_data = cache.get(cache_key)

    #     if cached_data is None:
    #         print("Запрос к базе данных, т.к. кэша нет")

    #         queryset = super().get_queryset(request)

    #         # Создаем копию queryset в виде списка, т.к. QuerySet нельзя закэшировать
    #         cached_data = list(queryset)

    #         cache.set(cache_key, cached_data, timeout=CACHE_TIMEOUT)  # Кэш на 15 минут
    #     else:
    #         print("Данные получены из кэша")

    #     #  Возвращаем queryset из закэшированных данных

    #     end_time = time.time()
    #     execution_time = end_time - start_time
    #     print(f"Время выполнения запроса: {execution_time:.4f} секунд")


    #     # Создаем QuerySet из кэшированных данных
    #     return Product.objects.filter(pk__in=[item.pk for item in cached_data])

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
    date_hierarchy = 'order_date'
    readonly_fields = ['order_date']
    raw_id_fields=['user', 'user_addresses']
    inlines = [OrderInline]
    search_fields = (
        'id',
        'user__full_name',
        'user__email'
    )
    # filter_horizontal = ('product',)  
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
