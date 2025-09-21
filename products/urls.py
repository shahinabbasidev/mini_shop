from django.urls import path
from . import views
from .views import ProductDetailView

app_name = 'products'

urlpatterns = [
    path('<int:pk>', ProductDetailView.as_view(), name='product-detail'),
]