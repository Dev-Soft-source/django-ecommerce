from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from dress.settings import BASE_URL
from django.http import HttpResponse

# Create your views here.

def admin_home(request):
    return render(request,"admins/home.html")

def admin_login(request):
    return render(request,"admins/signin.html")

def admin_logout(request):
    return render(request,"admins/logout.html")

def category_list(request):
    return render(request,"admins/category_list.html")

def category_create(request):
    return render(request,"admins/category_create.html")

def category_update(request, pk):
    return render(request,"admins/category_update.html")

def category_delete(request, pk):
    return render(request,"admins/category_delete.html")

def product_list(request):
    return render(request,"admins/product_list.html")

def product_create(request):
    return render(request,"admins/product_create.html")

def product_update(request, pk):
    return render(request,"admins/product_update.html")

def product_delete(request, pk):
    return render(request,"admins/product_delete.html")

def customer_list(request):
    return render(request,"admins/customer_list.html")

def customer_create(request):
    return render(request,"admins/customer_create.html")

def customer_update(request, pk):
    return render(request,"admins/customer_update.html")

def customer_delete(request, pk):
    return render(request,"admins/customer_delete.html")

def order_list(request):
    return render(request,"admins/order_list.html")

def order_create(request):
    return render(request,"admins/order_create.html")

def order_update(request, pk):
    return render(request,"admins/order_update.html")

def order_delete(request, pk):
    return render(request,"admins/order_delete.html")

def merchant_list(request):
    return render(request,"admins/merchant_list.html")

def merchant_create(request):
    return render(request,"admins/merchant_create.html")

def merchant_update(request, pk):
    return render(request,"admins/merchant_update.html")

def merchant_delete(request, pk):
    return render(request,"admins/merchant_delete.html")

def sub_category_list(request):
    return render(request,"admins/sub_category_list.html")

def sub_category_create(request):
    return render(request,"admins/sub_category_create.html")

def sub_category_update(request, pk):
    return render(request,"admins/sub_category_update.html")

def sub_category_delete(request, pk):
    return render(request,"admins/sub_category_delete.html")

def staff_list(request):
    return render(request,"admins/staff_list.html")

def staff_create(request):
    return render(request,"admins/staff_create.html")

def staff_update(request, pk):
    return render(request,"admins/staff_update.html")

def staff_delete(request, pk):
    return render(request,"admins/staff_delete.html")

@csrf_exempt
def file_upload(request):
    file=request.FILES["file"]
    fs=FileSystemStorage()
    filename=fs.save(file.name,file)
    file_url=fs.url(filename)
    return HttpResponse('{"location":"'+ BASE_URL +''+file_url+'"}')
