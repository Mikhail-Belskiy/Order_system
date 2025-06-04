from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


# Пользователь
class User(AbstractUser):
    is_supplier = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name='группы',
        blank=True,
        related_name='custom_user_set',
        help_text='Выберите группу(ы) для этого пользователя.'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='права',
        blank=True,
        related_name='custom_user_permissions_set',
        help_text='Выберите дополнительные права для этого пользователя.'
    )

# Поставщик
class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

# Категория и товар
class Category(models.Model):
    name = models.CharField(max_length=200)

class ProductProperty(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=200)
    product = models.ForeignKey('Product', related_name='properties', on_delete=models.CASCADE)

class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

# Заказ
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('created', 'создан'),
        ('confirmed', 'подтверждён'),
        ('shipped', 'отправлен'),
        ('closed', 'закрыт'),
    ], default='created')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)