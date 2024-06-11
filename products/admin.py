from django.contrib import admin
from .models import CategoryProducts, Products, Review, Order

admin.site.register(CategoryProducts)
admin.site.register(Products)
admin.site.register(Review)
admin.site.register(Order)

