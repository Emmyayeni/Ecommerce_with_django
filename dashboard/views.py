from django.shortcuts import render
from store.models import *
import json 
from store.utils import cartData
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import pandas as pd


# Create your views here.
class Dashboard(LoginRequiredMixin,View):
   login_url = 'login'    
   def get(self,request):
      data = cartData(request)
      cartItems = data['cartItems']
      order = data['order']
      items = data['items']
      products = Product.objects.all() 
      # print(items)
      products_item = items.values()
      # print(products_item)
      d1 = pd.DataFrame(products_item)

      df1 = [i.product.name for i in items]
      
      df = d1['quantity'].tolist()
      print(df1)
      print(df)
      
      context = {'items':items, 'order':order, 'cartItems':cartItems, 'all_product':products,'df':df,'df1':df1}
      return render(request,'dashboard\index.html',context)
