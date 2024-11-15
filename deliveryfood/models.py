from django.db import models

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=64, verbose_name='Название категории')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        
    def __str__(self):
        return self.category_name

# ТЕСТ КОММИТ
class Product(models.Model):
    name = models.CharField(max_length=64, verbose_name="Название")
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    description = models.CharField(max_length=512, verbose_name="Описание")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name
        


class Profile(models.Model):
    full_name = models.CharField(max_length=256, verbose_name='Полное имя')
    email = models.CharField(max_length=320, verbose_name='Email')
    phone = models.CharField(max_length=11, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.full_name


class Address(models.Model):
    id_user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
    address = models.CharField(max_length=512, verbose_name='Адрес')

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса' 

    def __str__(self):
        return self.address
       


class Order(models.Model):
    id_user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
    id_user_addresses = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='Адрес доставки')
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    # def __str__(self):
    #     return self.address


class OrderedItem(models.Model):
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    product_quantity = models.SmallIntegerField(default=0, verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'
