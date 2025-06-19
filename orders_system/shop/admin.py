from django.contrib import admin
from .models import *
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

admin.site.register([User, ProductProperty, Category, Supplier, Order, OrderItem, Cart, CartItem])

class ProductPropertyInline(admin.TabularInline):
    model = ProductProperty
    extra = 1

class ProductResource(resources.ModelResource):
    id = fields.Field(
        column_name='id',
        attribute='id'
    )
    name = fields.Field(
        attribute='name',
        column_name='Название товара'
    )
    supplier = fields.Field(
        column_name='Поставщик',
        attribute='supplier',
        widget=ForeignKeyWidget(Supplier, 'name')
    )
    category = fields.Field(
        column_name='Категория',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name')
    )
    price = fields.Field(
        attribute='price',
        column_name='Цена'
    )
    stock = fields.Field(
        attribute='stock',
        column_name='Остаток'
    )
    is_active = fields.Field(
        attribute='is_active',
        column_name='Активен'
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'supplier', 'category', 'price', 'stock', 'is_active')
        export_order = ('id', 'name', 'supplier', 'category', 'price', 'stock', 'is_active')

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    inlines = [ProductPropertyInline]

