from django import template
from ..models import Product, Order, Profile

register = template.Library()

@register.simple_tag
def product_count():
    """
    Возвращает количество товаров.
    """
    return Product.objects.count()

@register.simple_tag
def add_query_param(request, key, value):
    """
    Добавляет параметр запроса в URL.
    """
    url = request.GET.copy()
    url[key] = value
    return url.urlencode()

@register.simple_tag
def get_orders():
    """
    Возвращает все заказы с привязанными пользователями и адресами.
    """
    return Order.objects.select_related('user', 'user_addresses').all()

@register.simple_tag
def get_customers():
    """
    Возвращает всех пользователей с их заказами.
    """
    return Profile.objects.prefetch_related('order_set').all()

@register.inclusion_tag('product_list.html')
def show_products(category=None, min_price=None, max_price=None):
    """
    Возвращает список товаров с учетом фильтров.
    """
    products = Product.objects.all()
    if category:
        products = products.filter(category=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    return {'products': products}

@register.simple_tag
def get_filtered_products(category=None, min_price=None, max_price=None):
    """
    Возвращает отфильтрованный набор товаров.
    """
    products = Product.objects.all()
    if category:
        products = products.filter(category=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    return products

@register.simple_tag
def count_products_in_category(category):
    """
    Возвращает количество товаров в заданной категории.
    """
    return Product.objects.filter(category=category).count()