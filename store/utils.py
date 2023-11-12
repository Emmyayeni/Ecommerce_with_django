import json
from .models import *
from datetime import datetime

def cookieCart(request):
    # create empty for now for nono-logged in user
    try:
        cart = json.loads(request.COOKIES['cartc'])
    except:
        cart = {}
        print('CART:',cart)
    items = []
    order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
        # we use try block to prevent cart that have been removed from causing error
        try:
            if(cart[i]['quantity'] > 0): #with negative quantity = lot of freebies
               cartItems += cart[i]['quantity']
               product = Product.objects.get(id=i)
               total = (product.price * cart[i]['quantity']) 
               order['get_cart_total'] += total
               order['get_cart_items'] +=cart[i]['quantity']
               item = {
                   id:product.id,
                   'product':{'id': product.id,'name':product.name,'price':product.price,
                   'imageURL':product.imageURL},'quantity':cart[i]['quantity'],
                   'digital':product.digital,'get_total':total,
               }
               items.append(item)
        except:
            pass
    return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems':cartItems ,'order':order, 'items':items}


# def delete_cookie(request,key,path='/',domain=None,samesite=None):

#     set_cookie(cartc,max_age=0,domain=domain,samesite=samesite)
     

def guestOrder(request, user):
    customer = user.customer
    cookieData = cookieCart(request)
    items = cookieData['items']
        
    order,created = Order.objects.get_or_create(
		customer=customer,
		complete=False,
	)

    for item in items:
        products = item['product']
        product = Product.objects.get(id=products['id'])
        try:
            orderItem = OrderItem.objects.get(product=product)
        except:
            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                quantity=(item['quantity'] if item['quantity']>0 else -1*item['quantity']), # negative quantity = freebies
            )
        orderItem.quantity = (orderItem.quantity + item['quantity'])
        orderItem.save()
    order.save()
    
    # request.COOKIES['cartc'].delete()
    return user

print(datetime)
print(datetime.now())
