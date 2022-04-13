from django.urls import path
from . import views # from base project - crm1
# đây là nơi xử lý vụ: user nhập url, file này có nhiệm vụ gửi tín hiệu tới các views để show ra giao diện

urlpatterns = [
    path('register/', views.register_page, name="register"),
	path('login/', views.login_page, name="login"),  
	path('logout/', views.logout_user, name="logout"),
    
    path('', views.home, name="home"), # [base page, view connect to the base page]
    path('products/', views.products, name="products"),
    path('customer/<str:pk>/', views.customer, name="customer"), # this url is dynamic
    
    path('create_order/<str:pk>', views.create_order, name='create_order'),
    path('update_order/<str:pk>', views.update_order, name='update_order'),
    path('delete_order/<str:pk>', views.delete_order, name='delete_order')
]