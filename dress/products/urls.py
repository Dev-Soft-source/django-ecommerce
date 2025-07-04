from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.productList, name='product_list'),
    path('index/', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('shop-details/', views.shop_details, name='shop_details'),
    path('shopping-cart/', views.shopping_cart, name='shopping_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('blog-details/', views.blog_details, name='blog_details')
]
