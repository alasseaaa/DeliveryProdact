import re
from django.forms import ValidationError
from rest_framework import serializers
from .models import Product, Category, Profile, Address, Order, OrderedItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть меньше нуля.")
        return value
    
    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Описание должно содержать как минимум 10 символов.")
        return value
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Категория с таким названием уже существует.")
        return value
        

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

    def validate_email(self, value):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Введите корректный адрес электронной почты.")
        return value
    
    def validate_email(self, value):
        if Profile.objects.filter(email=value).exists():
            raise serializers.ValidationError("Этот адрес электронной почты уже используется.")
        return value

    def validate_phone(self, value):
        if not value.startswith('8'):
            raise serializers.ValidationError("Номер телефона должен начинаться с 8.")
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError("Телефон должен содержать 11 цифр.")
        return value
    
    def validate_full_name(self, value):
        if not re.match(r'^[A-Za-zА-Яа-яЁё\s-]+$', value):
            raise serializers.ValidationError("Полное имя может содержать только буквы и пробелы.")   


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

class OrderedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedItem
        fields = "__all__"