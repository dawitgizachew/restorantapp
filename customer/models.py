from django.db import models

# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    catagory = models.ManyToManyField('Catagory', related_name='item')
    
    def __str__(self):
        return self.name

class Catagory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class OrderModel(models.Model):
    created_on =models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    delivery_place = models.CharField(max_length=50, blank=True)
    transaction_number = models.CharField(max_length=100, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I:%M %p")}'

    