from django.contrib import admin

from .models import Category, Product, Profile, Address, Order, OrderedItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'category_name',
    ]

    search_fields = (
            "category_name",
        )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # отображение
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
    


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
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

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'address',
    ]
    
    search_fields = (
        'address',
        'user__full_name'
    )

class OrderInline(admin.TabularInline):
    model = OrderedItem
    raw_id_fields=['product',]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'user_addresses', 'order_date',]
    readonly_fields = ['order_date']
    raw_id_fields=['user', 'user_addresses']
    inlines = [OrderInline]
    search_fields = (
        'id',
    )
    
    
@admin.register(OrderedItem)
class OrderedItemAdmin(admin.ModelAdmin):
    list_display = [
        'order',
        'product',
        'product_quantity',
    ]

