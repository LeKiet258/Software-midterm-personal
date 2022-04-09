# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

# home page
def home(request):
    # tìm tới nơi mô tả cách 'Dashboard' (nơi này còn gọi là 'template') dc hiển thị lên màn hình & render nó
    return render(request, 'accounts/dashboard.html')  # render() làm cho chữ đẹp hơn (bằng việc tuân theo format htm)

def products(request):
    return render(request, 'accounts/products.html') 

# customer page
def customer(request):
    return render(request, 'accounts/customer.html') 