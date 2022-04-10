from django.forms import ModelForm
from .models import *

# create a custom form
class OrderForm(ModelForm):
    class Meta:
        model = Order # model to create form from
        fields = '__all__' # form with all attributes from class 'Order'
        