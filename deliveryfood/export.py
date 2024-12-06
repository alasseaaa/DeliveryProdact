from import_export.resources import ModelResource
from .models import Product, Category, Profile, Address, Order, OrderedItem

class ProductResource(ModelResource):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price']

class CategoryResource(ModelResource):
    class Meta:
        model = Category
        fields = ['category_name']

class ProfileResource(ModelResource):
    class Meta:
        model = Profile
        fields = ['full_name', 'email', 'phone']

class AddressResource(ModelResource):
    class Meta:
        model = Address
        fields = ['user', 'address']

class OrderResource(ModelResource):
    class Meta:
        model = Order
        fields = ['user', 'user_address', 'order_date', 'products']

class OrderedItemResource(ModelResource):
    class Meta:
        model = OrderedItem
        fields = ['order', 'product', 'product_quantity']

