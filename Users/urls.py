from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('register/verify/', views.verification, name="verification"),
    path('login/', views.login, name="login"),
]