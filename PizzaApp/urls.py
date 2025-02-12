from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_pizza/', views.create_pizza, name='create_pizza'),
    path('payment/<int:order_id>/', views.payment_view, name='payment'), 
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]
