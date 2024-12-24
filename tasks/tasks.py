from datetime import date
from django.core.mail import send_mail
from celery import shared_task
from deliveryfood.models import Product

@shared_task
def sale_november():
    """
    Периодическая задача, снижающая цену товаров на 15% 
    каждый 11 ноября, а затем восстанавливает ее 12 ноября.
    """
    today = date.today()
    november_11th = date(today.year, 11, 11)
    november_12th = date(today.year, 11, 12)

    products = Product.objects.all()

    # Применение скидки в 00:00 11 ноября каждого года
    if today != november_11th:
        for product in products:
            current_price = float(product.price)
            discount = float(current_price) * 0.5
            new_price = float(current_price) - discount
            product.price = new_price
            product.save()
            print(f"Цена для товара {product.name} снижена до {product.price}")

    # Возвращение исходной цены в 00:00 12 ноября каждого года
    if today == november_12th:
        for product in products:
            current_price = float(product.price)
            discount = float(current_price) * 0.5
            product.price += discount
            product.save()
            print(f"Цена для товара {product.name} восстановлена до {product.price}")




# """
# Задачи для django проекта. Периодические задачи (celery)
# """
# from datetime import date
# from django.core.mail import send_mail
# from celery import shared_task
# from deliveryfood.models import Product

# @shared_task
# def sale_november():
#     """
#     Периодическая задача, снижающая цену товаров на 15% 
#     каждый 11 ноября, а затем восстанавливает ее 12 ноября.
#     """
#     today = date.today()
#     november_11th = date(today.year, 11, 11)
#     november_12th = date(today.year, 11, 12)

#     products = Product.objects.all()
#     current_price = float(product.price)
#     discount = float(current_price) * 0.5

#     # Применение скидки в 00:00 11 ноября каждого года
#     if today == november_11th:
#         for product in products:
#             new_price = float(current_price) - discount
#             product.price = new_price
#             product.save()
#             print(f"Цена для товара {product.name} снижена до {product.price}")

#     # Возвращение исходной цены в 00:00 12 ноября каждого года
#     if today == november_12th:
#         for product in products:
#             product.price += discount
#             product.save()
#             print(f"Цена для товара {product.name} восстановлена до {product.price}")


