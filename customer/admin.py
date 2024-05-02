from django.contrib import admin
from .models import MenuItem, Catagory, OrderModel



# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Catagory)
admin.site.register(OrderModel)