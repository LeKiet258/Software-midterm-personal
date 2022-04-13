# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from matplotlib.style import context
from .models import *
from django.forms import inlineformset_factory
from .forms import OrderForm    
from .filters import OrderFilter
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

def register_page(request):
    form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def login_page(request):
    context = {}
    return render(request, 'accounts/login.html', context)

def logout_user(request):
	logout(request)
	return redirect('login')

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

def products(request):
    products = Product.objects.all() # query the db for all products
    return render(request, 'accounts/products.html', {'products': products}) # pass biến 'products' vào template html để dùng

# customer page
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {'customer': customer, 'orders': orders, 'order_count': order_count, 'myFilter': myFilter}
    
    return render(request, 'accounts/customer.html', context) 

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

def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    
    # quy trình delete
    if request.method == 'POST':
        order.delete()
        return redirect('/') 
    
    context={'item': order}
    return render(request, 'accounts/delete.html', context)

