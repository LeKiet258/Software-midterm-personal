# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from matplotlib.style import context
from .models import *
from django.forms import inlineformset_factory
from .forms import *
from .filters import OrderFilter
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group

@unauthenticated_user
def register_page(request):
    form = CreateUserForm() # django helps with register form
    if request.method == 'POST': # quăng input user nhập vào form
        form = CreateUserForm(request.POST) # check duplicate account + hash pw,...
        if form.is_valid(): 
            user = form.save()
            username = form.cleaned_data.get('username')
            # automatically assign users signing up as a customer
            group = Group.objects.get(name='customer')
            user.groups.add(group) # associate a user with a group
            # Added username because of error returning customer name if not added
            Customer.objects.create(
				user=user,
				name=user.username,
			)
   
            messages.success(request, 'Account was created for' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else: # user nhập sai account hoặc pw
            messages.info(request, 'Username OR password is incorrect')
        
    context = {}
    return render(request, 'accounts/login.html', context)

def logout_user(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers,
               'total_customers': total_customers, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    
    # tìm tới nơi mô tả cách 'Dashboard' (nơi này còn gọi là 'template') dc hiển thị lên màn hình & render nó
    return render(request, 'accounts/dashboard.html', context)  # render() làm cho chữ đẹp hơn (bằng việc tuân theo format htm)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all() # get orders of a user
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context = {'orders': orders, 'total_orders': total_orders, 
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()

	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all() # query the db for all products
    return render(request, 'accounts/products.html', {'products': products}) # pass biến 'products' vào template html để dùng

# customer page
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customer': customer, 'orders': orders, 'order_count': order_count, 'myFilter': myFilter}
    
    return render(request, 'accounts/customer.html', context) 

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10) # [parent model, child model]
    customer = Customer.objects.get(id=pk)
    # 'queryset': tránh reference tới thông tin order cũ khi đặt hàng mới
    formset = OrderFormSet(queryset = Order.objects.none() ,instance=customer)
   
    # xử lý sau khi bấm nút 'Submit' để đặt hàng
    if request.method == 'POST':
        # form = OrderForm(request.POST) # pass the info to 'OrderForm' object to handle
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save() # save the info passed in to the DB
            return redirect('/') # send us back to the 'main' template
        
    context = {'formset': formset}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order) # prefill a form bằng cách thao tác với tham số 'instance'. Còn hiểu theo kiểu: create form from an existing order 
    
    # quy trình save changes
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order) # save changes to THAT instance (i.e. 'order')
        if form.is_valid():
            form.save() 
            return redirect('/') 
    
    context = {'form': form}
    
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    
    # quy trình delete
    if request.method == 'POST':
        order.delete()
        return redirect('/') 
    
    context={'item': order}
    return render(request, 'accounts/delete.html', context)

