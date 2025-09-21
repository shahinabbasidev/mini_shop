from django.shortcuts import render
from django.views.generic import DetailView
from products.models import Product, Information


class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'
    model = Product



class InformationDetailView(DetailView):
    template_name = 'products/product_detail.html'
    model = Information