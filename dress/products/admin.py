from django.contrib import admin
from .models import Products, ProductMedia, ProductTransaction, ProductDetails, ProductAbout, ProductTags, ProductQuestions, ProductReviewVoting, ProductReviews, ProductVarient, ProductVarientItems
# Register your models here.

admin.site.register(Products)
admin.site.register(ProductMedia)
admin.site.register(ProductTransaction)
admin.site.register(ProductDetails)
admin.site.register(ProductAbout)
admin.site.register(ProductTags)
admin.site.register(ProductQuestions)
admin.site.register(ProductReviews)
admin.site.register(ProductReviewVoting)
admin.site.register(ProductVarient)
admin.site.register(ProductVarientItems)
