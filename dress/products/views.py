from django.shortcuts import render

# Create your views here.

def productList(request):
    return render(request, 'products/index.html')

def shop(request):
    return render(request, 'products/shop.html')

def about(request):
    return render(request, 'products/about.html')

def shop_details(request):
    return render(request, 'products/shop-details.html')

def shopping_cart(request):
    return render(request, 'products/shopping-cart.html')

def checkout(request):
    return render(request, 'products/checkout.html')

def blog(request):
    return render(request, 'products/blog.html')

def contact(request):
    return render(request, 'products/contact.html')

def faq(request):
    return render(request, 'products/faq.html')

def blog_details(request):
    return render(request, 'products/blog-details.html')

def index(request):
    return render(request, 'products/index.html')
