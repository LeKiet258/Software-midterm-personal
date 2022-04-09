from django.contrib import admin
# file admin.py giúp hiển thị database lên web

# Register your models here.
from .models import *
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)