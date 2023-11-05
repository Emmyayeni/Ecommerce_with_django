from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from .models import Account
from .forms import RegistrationForm
from django.contrib import messages
from store.models import Customer,Product
from store.utils import guestOrder
# from store.utils import guestOrder 
from django.views import View
# Create your views here.


class Login(View):
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'account/snippets/login.html')
    
    def post(self,request):
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = Account.objects.get(email=email)

        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            user = guestOrder(request,user)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')
        return render(request, 'account/snippets/login.html')
        

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('home')

class Register(View):
    form = RegistrationForm()
    def get(self,request):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request,'account/snippets/register.html',{'form':self.form})

    def post(self,request):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email,password=raw_password)
            usern = guestOrder(request,account)
            login(request, usern)
            customer = Customer.objects.create(user=account)
            customer.save()
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
            return render(request,'account/snippets/register.html',{'form':self.form})


