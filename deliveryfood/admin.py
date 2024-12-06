from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from .models import Category, Product, Profile, Address, Order, OrderedItem
from .export import AddressResource, CategoryResource, OrderResource, OrderedItemResource, ProductResource, ProfileResource
from simple_history.admin import SimpleHistoryAdmin

@admin.register(Category)
class CategoryAdmin(SimpleHistoryAdmin, ExportActionModelAdmin):
    list_display = [
        'category_name',
    ]

    search_fields = (
            "category_name",
        )
    resource_class = CategoryResource   

@admin.register(Product)
class ProductAdmin(SimpleHistoryAdmin, ExportActionModelAdmin):
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
    resource_class = ProductResource
    


@admin.register(Profile)
class ProfileAdmin(SimpleHistoryAdmin, ExportActionModelAdmin):
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
    list_display = [
        'user',
        'address',
    ]
    
    search_fields = (
        'address',
        'user__full_name'
    )
    resource_class = AddressResource

class OrderInline(admin.TabularInline):
    model = OrderedItem
    raw_id_fields=['product',]

@admin.register(Order)
class OrderAdmin(SimpleHistoryAdmin, ExportActionModelAdmin):
    list_display = ['id', 'user', 'user_addresses', 'order_date',]
    readonly_fields = ['order_date']
    raw_id_fields=['user', 'user_addresses']
    inlines = [OrderInline]
    search_fields = (
        'id',
    )
    resource_class = OrderResource
    
@admin.register(OrderedItem)
class OrderedItemAdmin(SimpleHistoryAdmin, ExportActionModelAdmin):
    list_display = [
        'order',
        'product',
        'product_quantity',
    ]
    resource_class = OrderedItemResource   
