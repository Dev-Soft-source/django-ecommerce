from django.contrib import admin
from .models import CustomUser, CustomerUser, AdminUser, StaffUser, MerchantUser
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(AdminUser)
admin.site.register(StaffUser)
admin.site.register(MerchantUser)
admin.site.register(CustomerUser)
