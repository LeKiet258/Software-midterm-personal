from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user'] # the customer is able to modify his own info, but not 'user' attrib (thay would not see this attrib)
  
# create a custom form
class OrderForm(ModelForm):
    class Meta:
        model = Order # model to create form from
        fields = '__all__' # form with all attributes from class 'Order'
        
class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
        