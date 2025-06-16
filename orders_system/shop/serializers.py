from rest_framework import serializers
from .models import *

class ProductPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductProperty
        fields = ("name", "value")

class ProductSerializer(serializers.ModelSerializer):
    properties = ProductPropertySerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'supplier', 'category', 'price', 'stock', 'is_active', 'properties')

    def create(self, validated_data):
        properties = validated_data.pop('properties', [])
        product = Product.objects.create(**validated_data)
        for prop in properties:
            ProductProperty.objects.create(product=product, **prop)
        return product

    def update(self, instance, validated_data):
        properties = validated_data.pop('properties', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        for prop in properties:
            ProductProperty.objects.update_or_create(product=instance, name=prop['name'], defaults=prop)
        return instance

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ("product", "quantity", "price")

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "customer", "date", "status", "items")

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item in items_data:
            OrderItem.objects.create(order=order, **item)
        return order

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user