"""
Модуль для экспорта данных моделей приложения deliveryfood.
"""
from import_export.resources import ModelResource
from .models import Product, Category, Profile, Address, Order, OrderedItem

class ProductResource(ModelResource):
    """
    Ресурс для модели Product.
    """
    class Meta:
        """
        Метаданные ресурса:
        - model: Модель, с которой связан ресурс.
        - fields: Список полей, которые будут включены в экспорт.
        """
        model = Product
        fields = ['name', 'category', 'description', 'price']

    def dehydrate_price(self, Product):
        """
        Форматирует цену продукта.
        """
        return f"${Product.price:.2f}"

class CategoryResource(ModelResource):
    """
    Ресурс для модели Category.
    """
    class Meta:
        """
        Метаданные ресурса:
        - model: Модель, с которой связан ресурс.
        - fields: Список полей, которые будут включены в экспорт.
        """
        model = Category
        fields = ['category_name']

    def dehydrate_category_name(self, Category):
        """
        Форматирует название категории.
        """
        return Category.category_name.lower()

class ProfileResource(ModelResource):
    """
    Ресурс для модели Profile.
    """
    class Meta:
        """
        Метаданные ресурса:
        - model: Модель, с которой связан ресурс.
        - fields: Список полей, которые будут включены в экспорт.
        """
        model = Profile
        fields = ['full_name', 'email', 'phone']

class AddressResource(ModelResource):
    """
    Ресурс для модели Address.
    """
    class Meta:
        """
        Метаданные ресурса:
        - model: Модель, с которой связан ресурс.
        - fields: Список полей, которые будут включены в экспорт.
        """
        model = Address
        fields = ['user', 'address']

    def dehydrate_address(self, Address):
        """
        Форматирует адрес.
        """
        return Address.address.title()

class OrderResource(ModelResource):
    """
    Ресурс для модели Order.
    """
    class Meta:
        """
        Метаданные ресурса:
        - model: Модель, с которой связан ресурс.
        - fields: Список полей, которые будут включены в экспорт.
        """
        model = Order
        fields = ['user', 'user_address', 'order_date', 'products']

    def dehydrate_order_date(self, Order):
        """
        Форматирует дату заказа.
        """
        return Order.order_date.strftime("%Y-%m-%d")

class OrderedItemResource(ModelResource):
    """
    Ресурс для модели OrderedItem.
    """
    class Meta:
        """
        Метаданные ресурса:
        - model: Модель, с которой связан ресурс.
        - fields: Список полей, которые будут включены в экспорт.
        """
        model = OrderedItem
        fields = ['order', 'product', 'product_quantity']

    def dehydrate_product_quantity(self, OrderedItem):
        """
        Форматирует количество товара.
        """
        return f'{OrderedItem.product_quantity} шт.'
