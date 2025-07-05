from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_home, name='admin_home'),

    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),    

    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/update/', views.order_update, name='order_update'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),

    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/update/', views.customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),

    path('sub_categories/', views.sub_category_list, name='sub_category_list'),
    path('sub_categories/create/', views.sub_category_create, name='sub_category_create'),
    path('sub_categories/<int:pk>/update/', views.sub_category_update, name='sub_category_update'),
    path('sub_categories/<int:pk>/delete/', views.sub_category_delete, name='sub_category_delete'),

    path('merchants/', views.merchant_list, name='merchant_list'),
    path('merchants/create/', views.merchant_create, name='merchant_create'),
    path('merchants/<int:pk>/update/', views.merchant_update, name='merchant_update'),
    path('merchants/<int:pk>/delete/', views.merchant_delete, name='merchant_delete'),

    path('staffs/', views.staff_list, name='staff_list'),
    path('staffs/create/', views.staff_create, name='staff_create'),
    path('staffs/<int:pk>/update/', views.staff_update, name='staff_update'),
    path('staffs/<int:pk>/delete/', views.staff_delete, name='staff_delete'),

    path('file_upload/', views.file_upload, name='file_upload'),

]