from django.urls import path
from store.views import *

urlpatterns = [
    path('store',Store.as_view(),name='store'),
    path('checkout',Checkout.as_view(),name='checkout'),
    path('cart',Cart.as_view(),name='cart'),
    path('update_item/',updateItem,name='update_item'),
    path('single_view/<pk>/',SingleView.as_view(),name='single_view'),
]
