from django.shortcuts import render, redirect
from .models import *
from .forms import UserRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import View
from django.db.models import Q
from django.http import JsonResponse
import json

# Create your views here.
def index(request):
    if 'search' in request.GET:
        search = request.GET['search']
        product = Product.objects.filter(name__icontains=search)
    else:
        product = Product.objects.all()
    categories = Category.objects.all()
    data = {'product':product, 'categories':categories}
    return render(request, 'index.html', data) 


def showcategory(request, cid):
    categories = Category.objects.all()
    cats = Category.objects.get(pk=cid)
    product = Product.objects.filter(cat=cats)
    data = {
        'categories':categories,
        'product':product
    }
    return render(request, 'index.html', data)


    # if request.method == 'GET':
    #     category_id = request.GET.get('category_id')
    #     #print(category_id)
    #     product = Product.objects.filter(Q(cat=category_id)).values()
    #     # for p in product:
    #     #     #product = p.values()
    #     product=json.dumps(list(product.values()))
    #     print(product)
    #         #print(product)
    #     data ={
    #         'product':product,
    #     }
    #     print(data)
    #     return JsonResponse(data)
    #     #print(data)    

    

        



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Account Register Successfully')
            form.save()
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form':form})




class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'profile.html', {'form':form})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name=name, address=address, city=city, state=state, zipcode=zipcode)
            reg.save()
        return render(request, 'profile.html',{'form':form})



def address(request):
    address = Customer.objects.filter(user=request.user)
    return render(request, 'address.html', {'address':address})



def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    #print(product_id)
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/show_cart')



def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user).order_by('-id')

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        #print(cart_product)
        if cart_product:
            for p in cart_product:
                subtotal = (p.quantity * p.product.selling_price)
                amount += subtotal
                total_amount = amount + shipping_amount
            return render(request, 'addtocart.html', {'cart':cart, 'total_amount':total_amount, 'amount':amount})
        else:
            return render(request, 'emptycart.html')
    


def pluscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product = prod_id) & Q(user = request.user))
        c.quantity += 1
        c.save()

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            subtotal = (p.quantity * p.product.selling_price)
            amount += subtotal

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'total_amount':amount + shipping_amount
        }
        return JsonResponse(data)

        
def minuscart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()

        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            subtotal = (p.quantity * p.product.selling_price)
            amount += subtotal
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'total_amount':amount + shipping_amount
        }
        return JsonResponse(data)
    

def checkout(request):
    address = Customer.objects.filter(user=request.user)
    cart = Cart.objects.filter(user=request.user)
    
    amount = 0.0
    shipping_amount = 70.0
    total_amount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            subtotal = (p.quantity * p.product.selling_price)
            amount += subtotal
            total_amount = amount + shipping_amount
    return render(request, 'checkout.html', {'address':address, 'cart':cart,'subtotal':subtotal, 'total_amount':total_amount, 'amount':amount, 'shipping_amount':shipping_amount})


