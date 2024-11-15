from django.contrib import admin

from .models import Category, Product, Profile, Address, Order, OrderedItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'category_name',
    ]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # отображение
    list_display = [
        'name',
        'id_category',
        'kratkoye_opisanie',
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

    def kratkoye_opisanie(self, obj):
        """
        Возвращает краткое описание объекта.
        Описание объекта, сокращенное до первых пятидесяти символов.
        """
        return (
            obj.description[:50] + "..."
            if len(obj.description) > 50
            else obj.description
        )
    


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'email',
        'phone',
    ]

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'id_user',
        'address',
    ]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id_user',
        'id_user_addresses',
        'order_date',
    ]

@admin.register(OrderedItem)
class OrderedItemAdmin(admin.ModelAdmin):
    list_display = [
        'id_order',
        'id_product',
        'product_quantity',
    ]