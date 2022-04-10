# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# home page
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
    context = {'customer': customer, 'orders': orders, 'order_count': order_count}
    
    return render(request, 'accounts/customer.html', context) 