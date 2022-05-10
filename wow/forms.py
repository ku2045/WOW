from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class CustomerForm(ModelForm):
  class Meta:
    model = RrskCustomers
    fields = ['cust_fname','cust_type','cust_lname','cust_phone_no','cust_country','cust_state','cust_city','cust_street','cust_no','cust_zip']
    exclude = ['user','cust_type']


class OrderForm(ModelForm):
  class Meta:
    model = RrskRental
    fields = ['pickup_date','dropoff_date','pickup_location','dropoff_location','start_odometer','end_odometer']

class OrderFormCreate(ModelForm):
	class Meta:
		model = RrskRental
		fields = ['pickup_date','dropoff_date','pickup_location','dropoff_location','start_odometer','end_odometer']


class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']

class PayForm(ModelForm):
  class Meta:
    model = RrskInvoicePayment
    fields = ['pay_amount','pay_date','pay_method','card_no',]

class CreateLocForm(ModelForm):
  class Meta:
    model = RrskLocation
    fields = ["loc_phone_no","loc_email","loc_country","loc_state","loc_city","loc_street","loc_no","loc_zip"]
    exclude = ['loc_country']
