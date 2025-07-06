from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('demo/',views.demoPage),
    path('',views.demoPageTemplate, name="admin_login"),
    path('admin_login_process/',views.adminLoginProcess,name="admin_login_process"),
    path('admin_logout_process/',views.adminLogoutProcess,name="admin_logout_process"),

    # PAGE FOR ADMIN
    path('admin_home/', views.admin_home,name="admin_home"),

    #CATEGORIES
    path('category_list/', views.CategoriesListView.as_view(),name="category_list"),
    path('category_create/', views.CategoriesCreate.as_view(),name="category_create"),
    path('category_update/<slug:pk>/', views.CategoriesUpdate.as_view(),name="category_update"),

    #SUBCATEGORIES
    path('sub_category_list/', views.SubCategoriesListView.as_view(),name="sub_category_list"),
    path('sub_category_create/', views.SubCategoriesCreate.as_view(),name="sub_category_create"),
    path('sub_category_update/<slug:pk>/', views.SubCategoriesUpdate.as_view(),name="sub_category_update"),

    #Merchant User
    path('merchant_create/', views.MerchantUserCreateView.as_view(),name="merchant_create"),
    path('merchant_list/', views.MerchantUserListView.as_view(),name="merchant_list"),
    path('merchant_update/<slug:pk>/', views.MerchantUserUpdateView.as_view(),name="merchant_update"),

    #Products
    path('product_create/', views.ProductView.as_view(),name="product_view"),
    path('product_list/', views.ProductListView.as_view(),name="product_list"),
    path('product_edit/<str:product_id>/', views.ProductEdit.as_view(),name="product_edit"),
    path('product_add_media/<str:product_id>/', views.ProductAddMedia.as_view(),name="product_add_media"),
    path('product_edit_media/<str:product_id>/', views.ProductEditMedia.as_view(),name="product_edit_media"),
    path('product_media_delete/<str:id>/', views.ProductMediaDelete.as_view(),name="product_media_delete"),
    path('product_add_stocks/<str:product_id>/', views.ProductAddStocks.as_view(),name="product_add_stocks"),
    path('file_upload/', views.file_upload,name="file_upload"),

    #Staff User
    path('staff_create/', views.StaffUserCreateView.as_view(),name="staff_create"),
    path('staff_list/', views.StaffUserListView.as_view(),name="staff_list"),
    path('staff_update/<slug:pk>/', views.StaffUserUpdateView.as_view(),name="staff_update"),

    #Customer User
    path('customer_create/', views.CustomerUserCreateView.as_view(),name="customer_create"),
    path('customer_list/', views.CustomerUserListView.as_view(),name="customer_list"),
    path('customer_update/<slug:pk>/', views.CustomerUserUpdateView.as_view(),name="customer_update"),


]