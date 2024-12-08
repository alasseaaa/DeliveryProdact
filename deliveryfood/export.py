from import_export.resources import ModelResource
from .models import Product, Category, Profile, Address, Order, OrderedItem

class ProductResource(ModelResource):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price']

    def dehydrate_price(self, Product):
        return f"${Product.price:.2f}"
    
class CategoryResource(ModelResource):
    class Meta:
        model = Category
        fields = ['category_name']
    
    def dehydrate_category_name(self, Category):
        return Category.category_name.lower()

class ProfileResource(ModelResource):
    class Meta:
        model = Profile
        fields = ['full_name', 'email', 'phone']

class AddressResource(ModelResource):
    class Meta:
        model = Address
        fields = ['user', 'address']

    def dehydrate_address(self, Address):
        return Address.address.title()

class OrderResource(ModelResource):
    class Meta:
        model = Order
        fields = ['user', 'user_address', 'order_date', 'products']

    def dehydrate_order_date(self, Order):
        return Order.order_date.strftime("%Y-%m-%d")

class OrderedItemResource(ModelResource):
    class Meta:
        model = OrderedItem
        fields = ['order', 'product', 'product_quantity']

    def dehydrate_product_quantity(self, OrderedItem):
        return f'{OrderedItem.product_quantity} шт.'

