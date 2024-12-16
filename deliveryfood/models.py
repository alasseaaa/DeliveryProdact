"""
Этот модуль содержит модели для django проекта.

"""
from django.db import models
from simple_history.models import HistoricalRecords

class Category(models.Model):
    """
    Модель для представления категории товаров.
    """
    category_name = models.CharField(max_length=64, verbose_name='Название категории')

    class Meta:
        """
        Мета-информация для модели Category.
        """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return str(self.category_name)

class Product(models.Model):
    """
    Модель для представления товаров.
    """
    name = models.CharField(max_length=64, verbose_name="Название")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    description = models.CharField(max_length=512, verbose_name="Описание")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    history = HistoricalRecords()

    class Meta:
        """
        Мета-информация для модели Product.
        """
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return str(self.name)

class Profile(models.Model):
    """
    Модель для представления профилей.
    """
    full_name = models.CharField(max_length=256, verbose_name='Полное имя')
    email = models.CharField(max_length=320, verbose_name='Email')
    phone = models.CharField(max_length=11, verbose_name='Телефон')
    history = HistoricalRecords()

    class Meta:
        """
        Мета-информация для модели Profile.
        """
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return str(self.full_name)

class Address(models.Model):
    """
    Модель для представления адресов заказчиков.
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
    address = models.CharField(max_length=512, verbose_name='Адрес')
    history = HistoricalRecords()

    class Meta:
        """
        Мета-информация для модели Address.
        """
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return str(self.address)

class Order(models.Model):
    """
    Модель для представления заказов.
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь')
    user_addresses = models.ForeignKey(
        Address, on_delete=models.CASCADE, verbose_name='Адрес доставки'
        )
    order_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    products = models.ManyToManyField(Product, through='OrderedItem')
    history = HistoricalRecords()

    class Meta:
        """
        Мета-информация для модели Order.
        """
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ № {self.id} от {self.user}'

class OrderedItem(models.Model):
    """
    Модель для представления заказанных товаров.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    product_quantity = models.SmallIntegerField(default=0, verbose_name='Количество')
    history = HistoricalRecords()

    class Meta:
        """
        Мета-информация для модели OrderedItem.
        """
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'
