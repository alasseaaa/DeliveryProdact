"""
Этот модуль содержит сериализаторы для моделей.

Он используется для преобразования данных моделей в формат, подходящий для 
REST API, а также для преобразования полученных данных обратно в модели. 
"""
import re
from rest_framework import serializers
from .models import Product, Category, Profile, Address, Order, OrderedItem

class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.

    Предоставляет возможность сериализации и десериализации данных модели
    Product в формате JSON.
    """
    class Meta:
        """
        Метаданные для сериализатора.

        model:  Указывает, к какой модели применяется сериализатор.
        fields:  Указывает, какие поля модели должны быть сериализованы.
                'all' - включает все поля модели.
        """
        model = Product
        fields = "__all__"

    def validate_price(self, value):
        """Проверка, что цена не меньше нуля."""
        if value < 0:
            raise serializers.ValidationError("Цена не может быть меньше нуля.")
        return value

    def validate_description(self, value):
        """Проверка, что описание содержит как минимум 10 символов."""
        if len(value) < 10:
            raise serializers.ValidationError("Описание должно содержать как минимум 10 символов.")
        return value

class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.

    Предоставляет возможность сериализации и десериализации данных модели
    Category в формате JSON.
    """
    class Meta:
        """
        Метаданные для сериализатора.

        model:  Указывает, к какой модели применяется сериализатор.
        fields:  Указывает, какие поля модели должны быть сериализованы.
                'all' - включает все поля модели.
        """
        model = Category
        fields = "__all__"

    def validate_name(self, value):
        """Проверка категории на уникальность."""
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Категория с таким названием уже существует.")
        return value

class ProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Profile.

    Предоставляет возможность сериализации и десериализации данных модели
    Profile в формате JSON.
    """
    class Meta:
        """
        Метаданные для сериализатора.

        model:  Указывает, к какой модели применяется сериализатор.
        fields:  Указывает, какие поля модели должны быть сериализованы.
                'all' - включает все поля модели.
        """
        model = Profile
        fields = "__all__"

    def validate_email(self, value):
        """Проверка корректности адреса электронной почты."""
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Введите корректный адрес электронной почты.")
        if Profile.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот адрес электронной почты уже используется.")
        return value

    def validate_phone(self, value):
        """Проверка номера телефона на соответствие формату."""
        if not value.startswith('8'):
            raise serializers.ValidationError("Номер телефона должен начинаться с 8.")
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("Телефон должен содержать 11 цифр.")
        return value

    def validate_full_name(self, value):
        """Проверка полного имени на допустимые символы."""
        if not re.match(r'^[A-Za-zА-Яа-яЁё\s-]+$', value):
            raise serializers.ValidationError("Полное имя может содержать только буквы и пробелы.")

class AddressSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Address.

    Предоставляет возможность сериализации и десериализации данных модели
    Address в формате JSON.
    """
    class Meta:

        model = Address
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Order.

    Предоставляет возможность сериализации и десериализации данных модели
    Order в формате JSON.
    """
    class Meta:
        """
        Метаданные для сериализатора.

        model:  Указывает, к какой модели применяется сериализатор.
        fields:  Указывает, какие поля модели должны быть сериализованы.
                'all' - включает все поля модели.
        """
        model = Order
        fields = "__all__"

class OrderedItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели OrderItem.

    Предоставляет возможность сериализации и десериализации данных модели
    OrderItem в формате JSON.
    """
    class Meta:
        """
        Метаданные для сериализатора.

        model:  Указывает, к какой модели применяется сериализатор.
        fields:  Указывает, какие поля модели должны быть сериализованы.
                'all' - включает все поля модели.
        """
        model = OrderedItem
        fields = "__all__"
