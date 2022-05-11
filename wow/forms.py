from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *

class CustomerForm(ModelForm):
  class Meta:
    model = SrkCustomers
    fields = ['cust_fname','cust_type','cust_lname','cust_phone_no','cust_country','cust_state','cust_city','cust_street','cust_no','cust_zip']
    exclude = ['user','cust_type']


class OrderForm(ModelForm):
  def disable_field(self):
        self.fields['start_odometer'].widget.attrs['readonly'] = True
        self.fields['pickup_date'].widget.attrs['readonly'] = True
        # self.fields['pickup_location'].widget.attrs['disabled'] = True
  
  class Meta:
    model = SrkRental
    fields = ['pickup_date','dropoff_date','pickup_location','dropoff_location','start_odometer','end_odometer']

class OrderFormCreate(ModelForm):
	class Meta:
		model = SrkRental
		fields = ['pickup_date','dropoff_date','pickup_location','dropoff_location','start_odometer','end_odometer']


class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']

class PayForm(ModelForm):
  class Meta:
    model = SrkInvoicePayment
    fields = ['pay_amount','pay_date','pay_method','card_no',]

class CreateLocForm(ModelForm):
  class Meta:
    model = SrkLocation
    fields = ["loc_phone_no","loc_email","loc_country","loc_state","loc_city","loc_street","loc_no","loc_zip"]
    exclude = ['loc_country']

class UpdateVehicleForm(ModelForm):
  class Meta:
    model = SrkVehicle
    fields = ["vin","v_make","v_model","liscence_plate_no","loc","v_class"]
    exclude = ['available']
class CreateVehicleForm(ModelForm):
  class Meta:
    model = SrkVehicle
    fields = ['vin', 'v_make', 'v_model', 'liscence_plate_no', 'available', 'v_class', 'loc']
    exclude = ['available']
