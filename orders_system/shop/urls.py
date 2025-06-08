from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet, SupplierOrderViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'supplier-orders', SupplierOrderViewSet, basename='supplier-orders')
urlpatterns = router.urls