from turtle import color
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

class CustomUser(AbstractUser):
    user_type_choices=((1,"Admin"),(2,"Staff"),(3,"Merchant"),(4,"Customer"))
    user_type=models.CharField(max_length=255,choices=user_type_choices,default=1)


class AdminUser(models.Model):
    profile_pic=models.FileField(default="")
    auth_user_id=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

class StaffUser(models.Model):
    profile_pic=models.FileField(default="")
    auth_user_id=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

class MerchantUser(models.Model):
    auth_user_id=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    profile_pic=models.FileField(default="")
    company_name=models.CharField(max_length=255)
    gst_details=models.CharField(max_length=255)
    address=models.TextField()
    is_added_by_admin=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class CustomerUser(models.Model):
    auth_user_id=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    profile_pic=models.FileField(default="")
    created_at=models.DateTimeField(auto_now_add=True)

class Badges(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)
    
    def get_absolute_url(self):
        return reverse("badge_list")

    def __str__(self):
        return self.title

class ProductColors(models.Model):
    id=models.AutoField(primary_key=True)
    color_name=models.CharField(max_length=15)
    color_code=models.CharField(max_length=7)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse("productcolor_list")

    def __str__(self):
        return self.color_name

class ProductSizes(models.Model):
    id=models.AutoField(primary_key=True)
    size_name=models.CharField(max_length=15)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

    def get_absolute_url(self):
        return reverse("productsize_list")

    def __str__(self):
        return self.size_name


@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminUser.objects.create(auth_user_id=instance)
        if instance.user_type==2:
            StaffUser.objects.create(auth_user_id=instance)
        if instance.user_type==3:
            MerchantUser.objects.create(auth_user_id=instance,company_name="",gst_details="",address="")
        if instance.user_type==4:
            CustomerUser.objects.create(auth_user_id=instance)            

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminuser.save()
    if instance.user_type==2:
        instance.staffuser.save()
    if instance.user_type==3:
        instance.merchantuser.save()
    if instance.user_type==4:
        instance.customeruser.save()

