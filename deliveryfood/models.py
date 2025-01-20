"""
Этот модуль содержит модели для django проекта.

"""
from django.db import models
from simple_history.models import HistoricalRecords
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

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

class ProductManager(models.Manager):
    def exclude_expensive(self):
        """
        Исключает товары с ценой больше 100.
        """
        return self.filter(price__lte=100)

class Product(models.Model):
    """
    Модель для представления товаров.
    """
    AVAILABILITY_CHOICES = [
        ('available', 'Доступно'),
        ('unavailable', 'Недоступно'),
    ]

    name = models.CharField(max_length=64, verbose_name="Название")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True, verbose_name="Изображение")
    description = models.CharField(max_length=512, verbose_name="Описание")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    file = models.FileField(upload_to='product_files/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    availability = models.CharField(max_length=12, choices=AVAILABILITY_CHOICES, verbose_name="Доступность")
    history = HistoricalRecords()

    objects = ProductManager()

    class Meta:
        """
        Мета-информация для модели Product.
        """
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['price']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'id': self.id})

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
        
    def save(self, *args, **kwargs):
        """
        Переопределение метода save для выполнения дополнительных действий.
        """
        commit = kwargs.pop('commit', True)
        if not self.full_name:
            self.full_name = f"{self.user.first_name} {self.user.last_name}"

        if commit:
            super().save(*args, **kwargs)

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
    order_date = models.DateTimeField(verbose_name='Дата заказа', default=timezone.now)
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

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'image', 'description', 'price', 'file', 'url', 'availability']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'price': forms.NumberInput(attrs={'min': 0}),
            'availability': forms.Select(choices=Product.AVAILABILITY_CHOICES),
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError('Цена должна быть больше нуля.')
        return price

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']
    
class BestSeller(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name='Товар')
    sales_count = models.IntegerField(verbose_name='Количество продаж')

    class Meta:
        verbose_name = 'Хит продаж'
        verbose_name_plural = 'Хиты продаж'

    def __str__(self):
        return f"{self.product.name} - {self.sales_count} продаж"
    
class StoreReview(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Профиль')
    review_text = models.TextField(verbose_name='Текст отзыва')
    rating = models.IntegerField(verbose_name='Рейтинг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отзыв о магазине'
        verbose_name_plural = 'Отзывы о магазине'

    def __str__(self):
        return f"Отзыв от {self.profile.full_name} - {self.rating} звезд"
    
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Профиль')
    review_text = models.TextField(verbose_name='Текст отзыва')
    rating = models.IntegerField(verbose_name='Рейтинг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отзыв о товаре'
        verbose_name_plural = 'Отзывы о товарах'

    def __str__(self):
        return f"Отзыв от {self.profile.full_name} на товар {self.product.name} - {self.rating} звезд"

class StoreReviewForm(forms.ModelForm):
    class Meta:
        model = StoreReview
        fields = ['review_text', 'rating']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 3}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5})
        }

class StoreFact(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Факт о магазине'
        verbose_name_plural = 'Факты о магазине'

    def __str__(self):
        return self.title
