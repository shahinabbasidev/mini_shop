from django.urls import path
from . import views


app_name = "Cart"

urlpatterns = [
    path('cash', views.CartDetailView.as_view(), name='cart_detail'),
]