#Проект создания заказов в интернет магазине

#Для запуска необходимо 
1. установить библиотеки из requirements.txt
2. создать миграции в базе `python manage.py migrate`
3. создать супер пользователя для админки `python manage.py createsuperuser`
4. запустить сервер `python manage.py runserver`

Доступно по:
http://127.0.0.1:8000/

5. В отдельном терминале запуск Celery worker :

`celery -A orders_system worker -l info`

#Админка 
http://127.0.0.1:8000/admin/

Импорт/экспорт товаров: через админку или эндпоинты /api/products/import_data/ и /api/products/export_data/

Для загрузки через админку можно использовать шаблон файла excel 
Если стоит в шаблоне id товара, происходит замена данных, если оставить пустым, то создаётся новый товар
![img.png](img.png)
[файл вложен в проект](template.xlsx)

Проверка email-рассылки
По умолчанию письма пишутся в консоль (EMAIL_BACKEND=console)

API

/register/	Регистрация

/login/	Вход

/products/	Список товаров

/cart/	Корзина

/checkout/	Оформл. заказа

/my-orders/	История заказов

[Ссылка](https://team44-9479.postman.co/workspace/orders_system~5e288222-baba-4258-a264-9f738c153e9e/collection/38564407-91e75a2c-42ea-4b65-9897-00c982f18fa2?action=share&source=copy-link&creator=38564407) на Postman для тестов API

