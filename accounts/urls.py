from django.urls import path
from . import views # from base project - crm1
# đây là nơi xử lý vụ: user nhập url, file này có nhiệm vụ gửi tín hiệu tới các views để show ra giao diện

urlpatterns = [
    path('', views.home), # [base page, view connect to the base page]
    path('products/', views.products),
    path('customer/', views.customer),
]