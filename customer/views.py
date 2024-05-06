import json
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, Catagory, OrderModel
# Create your views here.

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')



# ordering sys
class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item
        appetizers = MenuItem.objects.filter(catagory__name__contains='Appetizer')
        entres = MenuItem.objects.filter(catagory__name__contains='Entre')
        desserts = MenuItem.objects.filter(catagory__name__contains='Dessert')
        drinks = MenuItem.objects.filter(catagory__name__contains='Drink')
         

        # pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
        }
        # render the template
        return render(request, 'customer\order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        transaction_number = request.POST.get('transaction_number')
        delivery_place = request.POST.get('delivery_place')


        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price,
            }
            
            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            phone=phone,
            delivery_place=delivery_place,
            transaction_number=transaction_number,
            )
        order.items.add(*item_ids)


        # send confermation mail
        body = ('Thank you for your order! Your food is being made and will be delivered soon!\n'
            f'Your total: {price}\n'
            'Thank you again for your order!')

        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=True
        )
        context = {
            'items': order_items['items'],
            'price': price
            }

        return redirect('order-confirmation', pk=order.pk)





class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)


        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }
        
        return render(request, 'customer/order_confirmation.html', context)


    def post(self, request, pk, *args, **kwargs):
       
        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')


class OrderPayConfirmation(View):
    def get(self, reqiest, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')