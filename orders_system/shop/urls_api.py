from django.urls import path
from .views_api import (
    RegisterView, LoginView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),

]