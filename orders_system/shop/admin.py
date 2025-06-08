from django.contrib import admin
from .models import *

admin.site.register([User, Product, ProductProperty, Category, Supplier, Order, OrderItem])