from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.forms import inlineformset_factory
from .forms import OrderForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
# Create your views here.

@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username = username, password = password)
		if user is not None:
			login(request,user)
			return redirect('home')
		else:
			messages.info(request,'Username or password is incorrect')
	context={}
	return render(request,'accounts/login.html',context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = Order.objects.all()
	total_orders = orders.count()
	delivered_orders = orders.filter(status='Delivered').count()
	pending_orders = orders.filter(status ='Pending').count()
	context={'orders':orders,
				'total_orders':total_orders,
				'delivered_orders':delivered_orders,
				'pending_orders':pending_orders
			}
	return render(request,'accounts/user.html', context)

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)
			#Added username after video because of error returning customer name if not added
			Customer.objects.create(
				user=user,
				name=user.username,
				)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()
	total_orders = orders.count()
	total_customers = customers.count()
	delivered_orders = orders.filter(status='Delivered').count()
	pending_orders = orders.filter(status ='Pending').count()
	context = {'customers':customers, 'orders':orders ,'total_orders':total_orders, 'total_customers':total_customers,'delivered_orders':delivered_orders, 'pending_orders':pending_orders }
	return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
def about(request):
	return HttpResponse("about")

def products(request):
	products = Product.objects.all()
	return render(request,'accounts/products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request,pk):
	customer = Customer.objects.get(id = pk)
	orders = customer.order_set.all()
	order_count = orders.count()
	context = {
		'customer':customer,
		'orders':orders,
		'order_count':order_count
	}
	return render(request, 'accounts/customers.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('products','status'), extra = 3)
	customer = Customer.objects.get(id = pk)
	formset = OrderFormSet(queryset = Order.objects.none(),instance = customer)
	#form = OrderForm(initial = {'customer':customer})
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance = customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')
	
	context = {'formset':formset}
	return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
	order = Order.objects.get(id = pk)
	form = OrderForm(instance = order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance = order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}

	return render(request, 'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
	order = Order.objects.get(id = pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	context = {'item': order}

	return render(request, 'accounts/delete_order.html', context)
