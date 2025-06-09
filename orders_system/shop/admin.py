from django.contrib import admin
from .models import *

admin.site.register([User, ProductProperty, Category, Supplier, Order, OrderItem])

class ProductPropertyInline(admin.TabularInline):
    model = ProductProperty
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductPropertyInline]