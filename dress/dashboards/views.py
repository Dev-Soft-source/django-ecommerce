import re
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from products.models import Categories, SubCategories, ProductAbout, ProductDetails, ProductMedia, ProductTransaction, ProductTags, Products, ProductVarient
from .models import CustomUser, MerchantUser, StaffUser, CustomerUser, ProductColors, ProductSizes, Badges, InterfaceConfigures, InterfaceCollections, InterfaceBests, InterfaceHots, InterfaceNews, InterfaceInstagram
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db.models import Q
from dress.settings import BASE_URL, MEDIA_ROOT, MEDIA_URL
import os
from dress import settings


# Create your views here.
def demoPage(request):
    return HttpResponse("demo Page")

def demoPageTemplate(request):
    return render(request,"demo.html")

def adminLogin(request):
    return render(request,"admins/signin.html")

def adminLoginProcess(request):
    name=request.POST.get("name")
    password=request.POST.get("password")

    user=authenticate(username=name,password=password)

    if user is not None:
        login(request=request,user=user)
        return HttpResponseRedirect(reverse("admin_home"))
    else:
        messages.error(request,"Error in Login! Invalid Login Details!")
        return HttpResponseRedirect(reverse("admin_login"))

def adminLogoutProcess(request):
    logout(request)
    messages.success(request,"Logout Successfully!")
    return HttpResponseRedirect(reverse("admin_login"))

@login_required(login_url="/admin/")
def admin_home(request):
    return render(request,"admins/home.html")

#HOMEPAGE CONFIGS

class HomepageIndexView(ListView):
    def get(self, request, *args, **kwargs):
        products=Products.objects.filter(is_active=1)
        interface_configures=InterfaceConfigures.objects.all()
        collection_configures=InterfaceCollections.objects.all()
        best_products=InterfaceBests.objects.all()
        new_products=InterfaceNews.objects.all()
        hot_products=InterfaceHots.objects.all()
        instagram_products=InterfaceInstagram.objects.all()
        return render(request,"admins/homepage_index.html",{"products":products,"interface_configures":interface_configures,"collection_configures":collection_configures,"best_products":best_products,"new_products":new_products,"hot_products":hot_products,"instagram_products":instagram_products})

    def post(self,request,*args,**kwargs):
        interface_small_title_list=request.POST.getlist("interface_small_title[]")
        interface_title_list=request.POST.getlist("interface_title[]")
        interface_description_list=request.POST.getlist("interface_description[]")
        media_type_list=request.POST.getlist("media_type[]")
        configure_media_content_list=request.FILES.getlist("configure_media_content[]")

        collection_title_list=request.POST.getlist("collection_title[]")
        collection_media_type_list=request.POST.getlist("collection_media_type[]")
        collection_content_list=request.FILES.getlist("collection_media_content[]")

        best_product_list=request.POST.getlist("best_product[]")
        new_product_list = request.POST.getlist("new_product[]")
        hot_product_list = request.POST.getlist("hot_product[]")
        instagram_media_type_list = request.POST.getlist("instagram_media_type[]")
        instagram_media_content_list = request.FILES.getlist("instagram_media_content[]")       

        i=0
        for media_content in configure_media_content_list:
            fs = FileSystemStorage(location='static/img/hero/', base_url='/static/img/hero/')
            filename=fs.save(media_content.name, media_content)
            media_url=fs.url(filename)
            interface_configure=InterfaceConfigures(
                title=interface_title_list[i],
                small_title=interface_small_title_list[i],
                description=interface_description_list[i],
                media_type=media_type_list[i],
                media_content=media_url
            )
            interface_configure.save()
            i=i+1

        j=0
        for media_content in collection_content_list:
            fs = FileSystemStorage(location='static/img/banner/', base_url='/static/img/banner/')
            filename=fs.save(media_content.name, media_content)
            media_url=fs.url(filename)
            collection_configure=InterfaceCollections(
                title=collection_title_list[j],
                media_type=collection_media_type_list[j],
                media_content=media_url
            )
            collection_configure.save()
            j=j+1

        k = 0
        for product_id in best_product_list:
            try:
                product = Products.objects.get(id=product_id)  # Get the Products instance
                best_configure = InterfaceBests(
                    best_product=product  # Assign the instance, not just the ID
                )
                best_configure.save()
                k = k + 1
            except Products.DoesNotExist:
                print(f"Product with ID {product_id} not found")
                continue

        l = 0
        for product_id in new_product_list:
            try:
                product = Products.objects.get(id=product_id)
                new_configure = InterfaceNews(
                    new_product=product
                )
                new_configure.save()
                l = l + 1
            except Products.DoesNotExist:
                print(f"Product with ID {product_id} not found")
                continue

        m = 0
        for product_id in hot_product_list:
            try:
                product = Products.objects.get(id=product_id)
                hot_configure = InterfaceHots(
                    hot_product=product
                )
                hot_configure.save()
                m = m + 1
            except Products.DoesNotExist:
                print(f"Product with ID {product_id} not found")
                continue

        n=0
        for media_content in instagram_media_content_list:
            fs = FileSystemStorage(location='static/img/instagram/', base_url='/static/img/instagram/')
            filename=fs.save(media_content.name, media_content)
            media_url=fs.url(filename)
            instagram_configure=InterfaceInstagram(
                media_type=instagram_media_type_list[n],
                media_content=media_url
            )
            instagram_configure.save()
            n=n+1

        return HttpResponseRedirect(reverse("homepage_index"))


class ProductColorsListView(ListView):
    model=ProductColors
    template_name="admins/product_color_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=ProductColors.objects.filter(Q(color_name__contains=filter_val) | Q(color_code__contains=filter_val)).order_by(order_by)
        else:
            cat=ProductColors.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(ProductColorsListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=ProductColors._meta.get_fields()
        return context

class ProductColorsCreate(SuccessMessageMixin,CreateView):
    model=ProductColors
    success_message="Product Color Added!"
    fields="__all__"
    template_name="admins/product_color_create.html"

class ProductColorsUpdate(SuccessMessageMixin,UpdateView):
    model=ProductColors
    success_message="Product Color Updated!"
    fields="__all__"
    template_name="admins/product_color_update.html"

class ProductColorsDelete(View):
    def get(self,request,*args,**kwargs):
        _id=kwargs["pk"]
        category=ProductColors.objects.get(id=_id)   
        category.delete()
        return HttpResponseRedirect(reverse("productcolor_list"))


class ProductSizesListView(ListView):
    model=ProductSizes
    template_name="admins/product_size_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=ProductSizes.objects.filter(Q(size_name__contains=filter_val)).order_by(order_by)
        else:
            cat=ProductSizes.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(ProductSizesListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=ProductSizes._meta.get_fields()
        return context

class ProductSizesCreate(SuccessMessageMixin,CreateView):
    model=ProductSizes
    success_message="Product Size Added!"
    fields="__all__"
    template_name="admins/product_size_create.html"

class ProductSizesUpdate(SuccessMessageMixin,UpdateView):
    model=ProductSizes
    success_message="Product Size Updated!"
    fields="__all__"
    template_name="admins/product_size_update.html"

class ProductSizesDelete(View):
    def get(self,request,*args,**kwargs):
        _id=kwargs["pk"]
        category=ProductSizes.objects.get(id=_id)   
        category.delete()
        return HttpResponseRedirect(reverse("productsize_list"))


class BadgesListView(ListView):
    model=Badges
    template_name="admins/badge_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=Badges.objects.filter(Q(title__contains=filter_val)).order_by(order_by)
        else:
            cat=Badges.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(BadgesListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Badges._meta.get_fields()
        return context

class BadgesCreate(SuccessMessageMixin,CreateView):
    model=Badges
    success_message="Badge Added!"
    fields="__all__"
    template_name="admins/badge_create.html"    

class BadgesUpdate(SuccessMessageMixin,UpdateView):
    model=Badges
    success_message="Badge Updated!"
    fields="__all__"
    template_name="admins/badge_update.html"

class BadgesDelete(View):
    def get(self,request,*args,**kwargs):
        _id=kwargs["pk"]
        category=Badges.objects.get(id=_id)   
        category.delete()
        return HttpResponseRedirect(reverse("badge_list"))


class CategoriesListView(ListView):
    model=Categories
    template_name="admins/category_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=Categories.objects.filter(Q(title__contains=filter_val)).order_by(order_by)
        else:
            cat=Categories.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(CategoriesListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Categories._meta.get_fields()
        return context

class CategoriesCreate(SuccessMessageMixin,CreateView):
    model=Categories
    success_message="Category Added!"
    fields="__all__"
    template_name="admins/category_create.html"

class CategoriesUpdate(SuccessMessageMixin,UpdateView):
    model=Categories
    success_message="Category Updated!"
    fields="__all__"
    template_name="admins/category_update.html"

class CategoriesDelete(View):
    def get(self,request,*args,**kwargs):
        _id=kwargs["pk"]
        category=Categories.objects.get(id=_id)   
        category.delete()
        return HttpResponseRedirect(reverse("category_list"))


class SubCategoriesListView(ListView):
    model=SubCategories
    template_name="admins/sub_category_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=SubCategories.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=SubCategories.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(SubCategoriesListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=SubCategories._meta.get_fields()
        return context

class SubCategoriesCreate(SuccessMessageMixin,CreateView):
    model=SubCategories
    success_message="Sub Category Added!"
    fields="__all__"
    template_name="admins/sub_category_create.html"

class SubCategoriesUpdate(SuccessMessageMixin,UpdateView):
    model=SubCategories
    success_message="Sub Category Updated!"
    fields="__all__"
    template_name="admins/sub_category_update.html"

class MerchantUserListView(ListView):
    model=MerchantUser
    template_name="admins/merchant_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=MerchantUser.objects.filter(Q(auth_user_id__first_name__contains=filter_val) |Q(auth_user_id__last_name__contains=filter_val) | Q(auth_user_id__email__contains=filter_val) | Q(auth_user_id__username__contains=filter_val)).order_by(order_by)
        else:
            cat=MerchantUser.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(MerchantUserListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=MerchantUser._meta.get_fields()
        return context


class MerchantUserCreateView(SuccessMessageMixin,CreateView):
    template_name="admins/merchant_create.html"
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]

    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=3
        user.set_password(form.cleaned_data["password"])
        user.save()

        #Saving Merchant user
        profile_pic=self.request.FILES["profile_pic"]
        fs = FileSystemStorage(location='static/media/upload/', base_url='/static/media/upload/')
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)

        user.merchantuser.profile_pic=profile_pic_url
        user.merchantuser.company_name=self.request.POST.get("company_name")
        user.merchantuser.gst_details=self.request.POST.get("gst_details")
        user.merchantuser.address=self.request.POST.get("address")
        is_added_by_admin=False

        if self.request.POST.get("is_added_by_admin")=="on":
            is_added_by_admin=True

        user.merchantuser.is_added_by_admin=is_added_by_admin
        user.save()
        messages.success(self.request,"Merchant User Created")
        return HttpResponseRedirect(reverse("merchant_list"))

class MerchantUserUpdateView(SuccessMessageMixin,UpdateView):
    template_name="admins/merchant_update.html"
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        merchantuser=MerchantUser.objects.get(auth_user_id=self.object.pk)
        context["merchantuser"]=merchantuser
        return context

    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()

        #Saving Merchant user
        merchantuser=MerchantUser.objects.get(auth_user_id=user.id)
        if self.request.FILES.get("profile_pic",False):
            profile_pic=self.request.FILES["profile_pic"]
            fs = FileSystemStorage(location='static/media/upload/', base_url='/static/media/upload/')
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            merchantuser.profile_pic=profile_pic_url

        merchantuser.company_name=self.request.POST.get("company_name")
        merchantuser.gst_details=self.request.POST.get("gst_details")
        merchantuser.address=self.request.POST.get("address")
        is_added_by_admin=False

        if self.request.POST.get("is_added_by_admin")=="on":
            is_added_by_admin=True

        merchantuser.is_added_by_admin=is_added_by_admin
        merchantuser.save()
        messages.success(self.request,"Merchant User Updated")
        return HttpResponseRedirect(reverse("merchant_list"))
  
class ProductView(View):
    def get(self,request,*args,**kwargs):
        categories=Categories.objects.filter(is_active=1)
        categories_list=[]
        for category in categories:
            sub_category=SubCategories.objects.filter(is_active=1,category_id=category.id)
            categories_list.append({"category":category,"sub_category":sub_category})

        product_colors=ProductColors.objects.filter(is_active=1)
        product_sizes=ProductSizes.objects.filter(is_active=1)
        product_badges=Badges.objects.filter(is_active=1)

        merchant_users=MerchantUser.objects.filter(auth_user_id__is_active=True)

        return render(request,"admins/product_create.html",{"categories":categories_list,"merchant_users":merchant_users,"product_colors":product_colors,"product_sizes":product_sizes,"product_badges":product_badges})

    def post(self,request,*args,**kwargs):
        product_name=request.POST.get("product_name")
        brand=request.POST.get("brand")
        url_slug=request.POST.get("url_slug")
        sub_category=request.POST.get("sub_category")
        product_max_price=request.POST.get("product_max_price")
        product_discount_price=request.POST.get("product_discount_price")
        product_description=request.POST.get("product_description")
        added_by_merchant=request.POST.get("added_by_merchant")
        in_stock_total=request.POST.get("in_stock_total")
        media_type_list=request.POST.getlist("media_type[]")
        media_content_list=request.FILES.getlist("media_content[]")
        title_title_list=request.POST.getlist("title_title[]")
        title_details_list=request.POST.getlist("title_details[]")
        about_title_list=request.POST.getlist("about_title[]")
        about_details_list=request.POST.getlist("about_details[]")
        product_tags=request.POST.get("product_tags")
        long_desc=request.POST.get("long_desc")
        product_color=request.POST.get("product_color")
        product_size=request.POST.get("product_size")
        product_badge=request.POST.get("product_badge")
        is_active = request.POST.get("is_active")

        subcat_obj=SubCategories.objects.get(id=sub_category)
        color_obj=ProductColors.objects.get(id=product_color)
        size_obj=ProductSizes.objects.get(id=product_size)
        badge_obj=Badges.objects.get(id=product_badge)
        merchant_user_obj=MerchantUser.objects.get(id=added_by_merchant)
        product=Products(product_name=product_name,in_stock_total=in_stock_total,url_slug=url_slug,
                         brand=brand,subcategories_id=subcat_obj,product_description=product_description,
                         product_max_price=product_max_price,product_discount_price=product_discount_price,
                         product_long_description=long_desc,added_by_merchant=merchant_user_obj,is_active=is_active)
        product.save()

        product_obj=Products.objects.get(id=product.id)

        product_varients=ProductVarient(product_id=product_obj,
                                        color_id=color_obj,
                                        size_id=size_obj,
                                        badge_id=badge_obj)
        product_varients.save()

        i=0
        for media_content in media_content_list:
            fs = FileSystemStorage(location='static/media/upload/', base_url='/static/media/upload/')
            filename=fs.save(media_content.name, media_content)
            media_url=fs.url(filename)
            product_media=ProductMedia(product_id=product,media_type=media_type_list[i],media_content=media_url)
            product_media.save()
            i=i+1
        
        j=0
        for title_title in title_title_list:
            product_details=ProductDetails(title=title_title,title_details=title_details_list[j],product_id=product)
            product_details.save()
            j=j+1

        for about in about_title_list:
            product_about=ProductAbout(title=about, about_details=about_details_list[j],product_id=product)
            product_about.save()
            j=j+1

        product_tags_list=product_tags.split(",")

        for product_tag in product_tags_list:
            product_tag_obj=ProductTags(product_id=product,title=product_tag)
            product_tag_obj.save()
        
        product_transaction=ProductTransaction(product_id=product,transaction_type=1,transaction_product_count=in_stock_total,transaction_description="Intially Item Added in Stocks")
        product_transaction.save()
        return HttpResponseRedirect(reverse("product_list"))

@csrf_exempt
def file_upload(request):
    file=request.FILES["file"]
    fs = FileSystemStorage(location='static/media/upload/', base_url='/static/media/upload/')
    filename=fs.save(file.name,file)
    file_url=fs.url(filename)
    return HttpResponse('{"location":"'+BASE_URL+''+file_url+'"}')

class ProductListView(ListView):
    model=Products
    template_name="admins/product_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            products=Products.objects.filter(Q(product_name__contains=filter_val) | Q(product_description__contains=filter_val)).order_by(order_by)
        else:
            products=Products.objects.all().order_by(order_by)
        
        product_list=[]
        for product in products:
            product_media=ProductMedia.objects.filter(product_id=product.id,media_type=1,is_active=1).first()
            product_list.append({"product":product,"media":product_media})

        return product_list

    def get_context_data(self,**kwargs):
        context=super(ProductListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Products._meta.get_fields()
        return context

class ProductEdit(View):

    def get(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        product_details=ProductDetails.objects.filter(product_id=product_id)
        product_about=ProductAbout.objects.filter(product_id=product_id)
        product_tags=ProductTags.objects.filter(product_id=product_id)

        categories=Categories.objects.filter(is_active=1)
        categories_list=[]
        for category in categories:
            sub_category=SubCategories.objects.filter(is_active=1,category_id=category.id)
            categories_list.append({"category":category,"sub_category":sub_category})

        product_variant=ProductVarient.objects.filter(product_id=product_id).first()

        product_colors=ProductColors.objects.filter(id=product_variant.color_id.id,is_active=1)
        product_sizes=ProductSizes.objects.filter(id=product_variant.size_id.id,is_active=1)
        product_badges=Badges.objects.filter(id=product_variant.badge_id.id,is_active=1)

        merchant_users=MerchantUser.objects.filter(auth_user_id__is_active=True)

        return render(request,"admins/product_edit.html",{"categories":categories_list,"product":product,
                                                          "product_details":product_details,"product_about":product_about,"product_tags":product_tags,
                                                          "product_colors":product_colors,"product_sizes":product_sizes,"product_badges":product_badges,
                                                          "merchant_users":merchant_users})

    def post(self,request,*args,**kwargs):
        
        product_name=request.POST.get("product_name")
        brand=request.POST.get("brand")
        url_slug=request.POST.get("url_slug")
        sub_category=request.POST.get("sub_category")
        product_max_price=request.POST.get("product_max_price")
        product_discount_price=request.POST.get("product_discount_price")
        product_description=request.POST.get("product_description")
        title_title_list=request.POST.getlist("title_title[]")
        details_ids=request.POST.getlist("details_id[]")
        title_details_list=request.POST.getlist("title_details[]")
        about_title_list=request.POST.getlist("about_title[]")
        about_details_list=request.POST.getlist("about_details[]")
        about_ids=request.POST.getlist("about_id[]")
        product_tags=request.POST.get("product_tags")
        long_desc=request.POST.get("long_desc")
        product_color=request.POST.get("product_color")
        product_size=request.POST.get("product_size")
        product_badge=request.POST.get("product_badge")
        is_active=request.POST.get("is_active")
        subcat_obj=SubCategories.objects.get(id=sub_category)
        color_obj=ProductColors.objects.get(id=product_color)
        size_obj=ProductSizes.objects.get(id=product_size)
        badge_obj=Badges.objects.get(id=product_badge)

        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        product.product_name=product_name
        product.url_slug=url_slug
        product.brand=brand
        product.subcategories_id=subcat_obj
        product.product_description=product_description
        product.product_max_price=product_max_price
        product.product_discount_price=product_discount_price
        product.product_long_description=long_desc
        product.save()

        product_obj=Products.objects.get(id=product.id)

        product_varients=ProductVarient(product_id=product_obj,
                                        color_id=color_obj,
                                        size_id=size_obj,
                                        badge_id=badge_obj)
        product_varients.save()

        j=0
        for title_title in title_title_list:
            detail_id=details_ids[j]
            if detail_id == "blank" and title_title!="":
                product_details=ProductDetails(title=title_title,title_details=title_details_list[j],product_id=product)
                product_details.save()
            else: 
                if title_title!="":               
                    product_details=ProductDetails.objects.get(id=detail_id)
                    product_details.title=title_title
                    product_details.title_details=title_details_list[j]
                    product_details.product_id=product
                    product_details.save()
            j=j+1

        k=0
        for about in about_title_list:
            about_id=about_ids[k]
            if about_id=="blank" and about!="":
                product_about=ProductAbout(title=about,about_details=about_details_list[k],product_id=product)
                product_about.save()
            else:
                if about!="":
                    product_about=ProductAbout.objects.get(id=about_id)
                    product_about.title=about
                    product_about.about_details=about_details_list[k]
                    product_about.product_id=product
                    product_about.save()
            k=k+1
        
        ProductTags.objects.filter(product_id=product_id).delete()

        product_tags_list=product_tags.split(",")

        for product_tag in product_tags_list:
            product_tag_obj=ProductTags(product_id=product,title=product_tag)
            product_tag_obj.save()
        
        return HttpResponse("OK")
class ProductDelete(View):
    def get(self,request,*args,**kwargs):
        _id=kwargs["pk"]
        product=Products.objects.get(id=_id)   
        product.delete()
        return HttpResponseRedirect(reverse("product_list"))

class ProductAddMedia(View):
    def get(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        return render(request,"admins/product_add_media.html",{"product":product})

    def post(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        media_type_list=request.POST.getlist("media_type[]")
        media_content_list=request.FILES.getlist("media_content[]")
        
        i=0
        for media_content in media_content_list:
            fs = FileSystemStorage(location='static/media/upload/', base_url='/static/media/upload/')
            filename=fs.save(media_content.name,media_content)
            media_url=fs.url(filename)
            product_media=ProductMedia(product_id=product,media_type=media_type_list[i],media_content=media_url)
            product_media.save()
            i=i+1
        
        return HttpResponse("OK")

class ProductEditMedia(View):
    def get(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        product_medias=ProductMedia.objects.filter(product_id=product_id)
        return render(request,"admins/product_edit_media.html",{"product":product,"product_medias":product_medias})

class ProductMediaDelete(View):
    def get(self,request,*args,**kwargs):
        media_id=kwargs["id"]
        product_media=ProductMedia.objects.get(id=media_id)      

        file_path = os.path.join(MEDIA_ROOT, str(product_media.media_content).replace('/', os.sep))
        # Remove the file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)      
        product_id=product_media.product_id.id
        product_media.delete()
        return HttpResponseRedirect(reverse("product_edit_media",kwargs={"product_id":product_id}))

class ProductAddStocks(View):
    def get(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        return render(request,"admins/product_add_stocks.html",{"product":product})

    def post(self,request,*args,**kwargs):
        product_id=kwargs["product_id"]
        new_instock=request.POST.get("add_stocks")
        product=Products.objects.get(id=product_id)
        old_stocks=product.in_stock_total
        new_stocks=int(new_instock)+int(old_stocks)
        product.in_stock_total=new_stocks
        product.save()

        product_obj=Products.objects.get(id=product_id)
        product_transaction=ProductTransaction(product_id=product_obj,transaction_product_count=new_instock,transaction_description="New Product Added",transaction_type=1)
        product_transaction.save()
        return HttpResponseRedirect(reverse("product_add_stocks",kwargs={"product_id":product_id}))


class StaffUserListView(ListView):
    model=StaffUser
    template_name="admins/staff_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=StaffUser.objects.filter(Q(auth_user_id__first_name__contains=filter_val) |Q(auth_user_id__last_name__contains=filter_val) | Q(auth_user_id__email__contains=filter_val) | Q(auth_user_id__username__contains=filter_val)).order_by(order_by)
        else:
            cat=StaffUser.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(StaffUserListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=StaffUser._meta.get_fields()
        return context

class StaffUserCreateView(SuccessMessageMixin,CreateView):
    template_name="admins/staff_create.html"
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]

    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=2
        user.set_password(form.cleaned_data["password"])
        user.save()

        #Saving Merchant user
        profile_pic=self.request.FILES["profile_pic"]
        fs = FileSystemStorage(location='static/media/upload/', base_url='/static/media/upload/')
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)

        user.staffuser.profile_pic=profile_pic_url
        user.save()
        messages.success(self.request,"Staff User Created")
        return HttpResponseRedirect(reverse("staff_list"))

class StaffUserUpdateView(SuccessMessageMixin,UpdateView):
    template_name="admins/staff_update.html"
    model=CustomUser
    fields=["first_name","last_name","email","username"]

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        staffuser=StaffUser.objects.get(auth_user_id=self.object.pk)
        context["staffuser"]=staffuser
        return context

    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.save()

        #Saving Merchant user
        staffuser=StaffUser.objects.get(auth_user_id=user.id)
        if self.request.FILES.get("profile_pic",False):
            profile_pic=self.request.FILES["profile_pic"]
            fs = FileSystemStorage(location='static/media/upload/', base_url='/static/media/upload/')
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            staffuser.profile_pic=profile_pic_url

        staffuser.save()
        messages.success(self.request,"Staff User Updated")
        return HttpResponseRedirect(reverse("staff_list"))

class CustomerUserListView(ListView):
    model=CustomerUser
    template_name="admins/customer_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=CustomerUser.objects.filter(Q(auth_user_id__first_name__contains=filter_val) |Q(auth_user_id__last_name__contains=filter_val) | Q(auth_user_id__email__contains=filter_val) | Q(auth_user_id__username__contains=filter_val)).order_by(order_by)
        else:
            cat=CustomerUser.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(CustomerUserListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=CustomerUser._meta.get_fields()
        return context

class CustomerUserCreateView(SuccessMessageMixin,CreateView):
    template_name="admins/customer_create.html"
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]

    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=4
        user.set_password(form.cleaned_data["password"])
        user.save()

        #Saving Merchant user
        profile_pic=self.request.FILES["profile_pic"]
        fs = FileSystemStorage(location='static/media/upload/', base_url='/static/media/upload/')
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)

        user.customeruser.profile_pic=profile_pic_url
        user.save()
        messages.success(self.request,"Customer User Created")
        return HttpResponseRedirect(reverse("customer_list"))

class CustomerUserUpdateView(SuccessMessageMixin,UpdateView):
    template_name="admins/customer_update.html"
    model=CustomUser
    fields=["first_name","last_name","email","username"]

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        customeruser=CustomerUser.objects.get(auth_user_id=self.object.pk)
        context["CustomerUser"]=customeruser
        return context

    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.save()

        #Saving Merchant user
        customeruser=CustomerUser.objects.get(auth_user_id=user.id)
        if self.request.FILES.get("profile_pic",False):
            profile_pic=self.request.FILES["profile_pic"]
            fs = FileSystemStorage(location='static/media/upload/', base_url='/static/media/upload/')
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            customeruser.profile_pic=profile_pic_url

        customeruser.save()
        messages.success(self.request,"Customer User Updated")
        return HttpResponseRedirect(reverse("customer_list"))