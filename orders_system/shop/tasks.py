from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def send_order_email(order_id):
    order = Order.objects.get(id=order_id)
    send_mail(
        'Подтверждение заказа',
        f'Ваш заказ #{order.id} принят!',
        'shop@example.com',
        [order.customer.email]
    )
    send_mail(
        'Накладная',
        f'Заказ #{order.id} оформлен.',
        'shop@example.com',
        ['admin@example.com']
    )