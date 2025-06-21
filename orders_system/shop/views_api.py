from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Order, OrderItem, Supplier, Category, Cart, CartItem, Contact
from .serializers import (
    ProductSerializer,
    ContactSerializer,
    UserSerializer,
    CartSerializer,
    OrderHistorySerializer
)
from rest_framework import filters
from .tasks import send_order_email

User = get_user_model()

# Регистрация
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

#Вход
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Список товаров
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['supplier', 'category']
    search_fields = ['name', 'description']

# Корзина
# Получение корзины текущего пользователя
class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items', 'total_sum')

    def get_total_sum(self, obj):
        return sum(item.product.price * item.quantity for item in obj.items.all())

# Добавление товара в корзину
class AddToCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        return Response({'status': 'ok'})

    def delete(self, request):
        pid = str(request.data.get('product'))
        cart = request.session.get('cart', {})
        if pid in cart:
            del cart[pid]
            request.session['cart'] = cart
        return Response({'status': 'removed', 'cart': cart})

from rest_framework import serializers
# удаление из корзины
class RemoveFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        try:
            item = CartItem.objects.get(cart=cart, product_id=product_id)
            item.delete()
            return Response({"status": "removed"})
        except CartItem.DoesNotExist:
            return Response({"error": "not found"}, status=404)

class ContactView(generics.ListCreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
      serializer.save(user=self.request.user)

#  Подтверждение заказа
class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart_id = request.data.get('cart_id')
        contact_id = request.data.get('contact_id')
        try:
            cart = Cart.objects.get(id=cart_id, user=request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=404)
        try:
            contact = Contact.objects.get(id=contact_id, user=request.user)
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found'}, status=404)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=400)
        order = Order.objects.create(customer=request.user)
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order, product=item.product,
                quantity=item.quantity, price=item.product.price
            )
        cart.items.all().delete()  # Очистить корзину
        send_order_email.delay(order.id)
        return Response({'status': 'Заказ оформлен', 'order_id': order.id})

# Заказы пользователя
class UserOrdersView(generics.ListAPIView):
    serializer_class = OrderHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by('-date')