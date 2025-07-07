from django.shortcuts import render

# Create your views here.

def productList(request):
    context = {
        'home': 'active',
        'shop': '',
        'pages': '',
        'blog': '',
        'contact': ''
    }
    return render(request, 'products/index.html', context)

def shop(request):
    context = {
        'home': '',
        'shop': 'active',
        'pages': '',
        'blog': '',
        'contact': ''
    }
    return render(request, 'products/shop.html', context)

def about(request):
    context = {
        'home': '',
        'shop': '',
        'pages': 'active',
        'blog': '',
        'contact': ''
    }
    return render(request, 'products/about.html', context)

def shop_details(request):
    context = {
        'home': '',
        'shop': '',
        'pages': 'active',
        'blog': '',
        'contact': ''
    }
    return render(request, 'products/shop-details.html', context)

def shopping_cart(request):
    context = {
        'home': '',
        'shop': '',
        'pages': 'active',
        'blog': '',
        'contact': ''
    }
    return render(request, 'products/shopping-cart.html', context)

def checkout(request):
    context = {
        'home': '',
        'shop': '',
        'pages': 'active',
        'blog': '',
        'contact': ''
    }
    return render(request, 'products/checkout.html', context)

def blog(request):
    context = {
        'home': '',
        'shop': '',
        'pages': '',
        'blog': 'active',
        'contact': ''
    }
    return render(request, 'products/blog.html', context)

def contact(request):
    context = {
        'home': '',
        'shop': '',
        'pages': '',
        'blog': '',
        'contact': 'active'
    }
    return render(request, 'products/contact.html', context)

def faq(request):
    context = {
        'home': '',
        'shop': '',
        'pages': '',
        'blog': '',
        'contact': ''
    }
    return render(request, 'products/faq.html', context)

def blog_details(request):
    context = {
        'home': '',
        'shop': '',
        'pages': '',
        'blog': 'active',
        'contact': ''
    }
    return render(request, 'products/blog-details.html', context)

def index(request):
    context = {
        'home': 'active',
        'shop': '',
        'pages': '',
        'blog': '',
        'contact': ''
    }
    return render(request, 'products/index.html', context)
