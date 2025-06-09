from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *
from .tasks import send_order_email
import pandas as pd
from django.core.files.storage import default_storage
from django.http import FileResponse


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('properties').all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['supplier', 'category', 'is_active']
    search_fields = ['name']

    @action(detail=False, methods=['post'])
    def import_data(self, request):
        file = request.FILES['file']
        df = pd.read_csv(file)
        for row in df.to_dict(orient='records'):
            supplier = Supplier.objects.get(pk=row["supplier"])
            prod = Product.objects.create(
                supplier=supplier, name=row["name"], category=Category.objects.get_or_create(name=row["category"])[0],
                price=row["price"], stock=row["stock"], is_active=row["is_active"])
        return Response({'status': 'импорт завершён'}, status=201)

    @action(detail=False, methods=['get'])
    def export_data(self, request):
        products = Product.objects.all().values()
        df = pd.DataFrame(products)
        path = "products_export.csv"
        df.to_csv(path, index=False)
        response = FileResponse(open(path, 'rb'))
        return response


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.save(customer=self.request.user)
        send_order_email.delay(order.id)


class SupplierOrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        supplier = Supplier.objects.get(user=self.request.user)
        return Order.objects.filter(items__product__supplier=supplier).distinct()