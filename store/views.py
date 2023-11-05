from django.shortcuts import render
from .models import *
import json
from .utils import cartData
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.



class Home(View):
    def get(self,request):
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        products = Product.objects.all()
        context = {'items':items, 'order':order, 'cartItems':cartItems, 'all_product':products}

        return render(request,'home.html', context)

class Store(View):
    def get(self,request):
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        products = Product.objects.all()
        context = {'all_product':products,'cartItems':cartItems}
        return render(request,'store/store.html',context)
    
class SingleView(View):
    def get(self, request,*args,**kwargs):
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        id = kwargs.get('pk')
        product = Product.objects.get(id=id)
        context = {'product': product,'cartItems':cartItems}
        return render(request,'store/single_view.html',context)

class Checkout(LoginRequiredMixin,View):
    login_url = '/login'
    shipping_info_add = False
    def get(self,request):
        user = request.user.customer
        try:
            shipping_info = ShippingAddress.objects.get(customer=user)
            self.shipping_info_add = True
        except ShippingAddress.DoesNotExist:
            self.shipping_info_add = False
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        context = {'items':items, 'order':order, 'cartItems':cartItems,'shipping': self.shipping_info_add}
        return render(request, 'store/checkout.html',context)
    
class Cart(View):
    def get(self,request):
        data = cartData(request)

        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        context = {'items':items, 'order':order, 'cartItems':cartItems}

        return render(request, 'store/cart.html',context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
