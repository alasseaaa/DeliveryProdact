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
