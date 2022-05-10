from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User

# Create your views here.
from .models import *
from .decorators import unauthenticated_user
from .forms import *
import datetime

import sys
import os
import django
import random



def index(request):
  return render(request,'wow/index.html')

# @unauthenticated_user
@login_required(login_url = 'login')
def cars(request,pk):
  pk = int(pk)
  cars = RrskVehicle.objects.all()
  vehicles = random.choices(RrskVehicleClass.objects.raw('SELECT a.id, b.id as vid, b.v_make, b.v_model, a.class_name, a.daily_rate, a.daily_mileage_limit, a.over_mileage_fee FROM rrsk_vehicle_class a JOIN rrsk_vehicle b ON a.id = b.v_class_id'),k=20)
  print(vehicles)
  context = {'vehicles':vehicles,'id':pk}

  return render(request,'wow/cars.html',context)


@unauthenticated_user
def loginPage(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password =request.POST.get('password')
    nextUrl = request.POST.get('next')
    # print("--nextUrl ",nextUrl)
    user = authenticate(request, username=username, password=password)
    us = RrskCustomers.objects.get(user__username=username)
    print(us)
    if user is not None:
      login(request, user)
      
      if(username == "admin"):
        return redirect('/admindashboard/')

      return redirect('/dashboard/' + str(us.id))
    else:
      messages.info(request, 'Username OR password is incorrect')
    # u = User.objects.get(username=username)
    # u.set_password(password)
    # u.save()
  context = {}
  return render(request, 'wow/login.html', context)

@unauthenticated_user
def registerPage(request):
  form = CustomerForm()
  form1 = CreateUserForm()
  # form.fields['cust_type'].hidden = True
  if request.method == 'POST':
    form1 = CreateUserForm(request.POST)
    form = CustomerForm(request.POST)
    
    form.id = id
    if form.is_valid() and form1.is_valid():
      customer = form.save()
      is_corp_cust = False
      cust_email = request.POST.dict().get('email')
      at_index = cust_email.index("@")
      dot_index = cust_email.index(".")
      email_domain = cust_email[at_index+1:dot_index]
      corpnames = RrskCorporation.objects.raw('SELECT id, LOWER(corp_name) corp_name FROM `rrsk_corporation`; ')
      for i in range(len(corpnames)):
        cname = corpnames[i].corp_name
        cname = cname.replace(" ", "")
        if(email_domain == cname):
          is_corp_cust = True
          break
      customer.cust_type = 'C' if is_corp_cust else 'I'
      user = form1.save()
      customer.user = user
      customer.save()
      user.save()

      user_name = form.cleaned_data.get('cust_fname')
      # RrskCustomers.objects.create(user=user)

      # newuser = User.objects.create_user(form.cleaned_data.get('cust_fname'),form1.cleaned_data.get('email'), form1.cleaned_data.get('password1'))
      # newuser.save()
      

      messages.success(request, 'Account was created for ' + user_name)

      return redirect('login')


  context = {'form':form, 'form1': form1}
  return render(request, 'wow/register.html', context)


def dashboard(request, pk_test):
    pk_test = int(pk_test)
    print(pk_test)
    past_orders = RrskRental.objects.filter(cust=pk_test,
                                            end_odometer__isnull=False)  # .filter(dropoff_date__lte = datetime.date(2020, 12, 17))
    if len(past_orders) > 0:
        past_orders = RrskInvoice.objects.filter(rental__cust__id=pk_test)  #
        # past_orders.refresh_from_db()
    print(past_orders)
    pays = []
    lp = RrskInvoicePayment.objects.all()
    for it in lp:
        print(it.invoice_no.id)
        pays.append(int(it.invoice_no.id))
    pay_pending = RrskInvoice.objects.filter(rental__cust__id=pk_test, id__isnull=False)
    pay_paid = RrskInvoicePayment.objects.filter(invoice_no_id__rental__cust__id=pk_test)
    delivered = len(past_orders)
    curr_orders = RrskRental.objects.filter(cust=pk_test, end_odometer__isnull=True)
    print(curr_orders)
    pending = len(curr_orders)
    total_orders = delivered + pending
    payment_pending = len(pay_pending)
    payment_paid = len(pay_paid)
    payment_due = payment_pending - payment_paid
    context = {'past_orders': past_orders, 'curr_orders': curr_orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending, 'id': pk_test, 'pays': pays,
               'payment_pending': payment_pending, 'payment_paid':payment_paid, 'payment_due': payment_due}
    #context = {'past_orders': past_orders, 'curr_orders': curr_orders, 'total_orders': total_orders,
    #'delivered': delivered, 'pending': pending, 'id': pk_test, 'pays': pays
     #}
    return render(request, 'wow/dashboard.html', context)

@login_required(login_url = 'login')
def createOrder(request, pk , vid):
  customer = RrskCustomers.objects.get(id=pk)
  # print(RrskVehicle.objects.get('SELECT b.v_model FROM rrsk_vehicle b where b.id = 49'))
  qres = RrskVehicle.objects.filter(id=vid)
  vname = qres[0].v_model
  print(vname)
  form = OrderFormCreate(instance=customer)
  # print("form before post",form)
  if request.method == 'POST':
    form = OrderFormCreate(request.POST)
    if form.is_valid():
      rental = form.save()
      rental.refresh_from_db()
      rental.start_odometer = form.cleaned_data.get('start_odometer')
      rental.cust = customer
      car = request.POST.get('model')
      print('Model =  ', car)
      rental.v = random.choice(RrskVehicle.objects.filter(v_model= car))
      rental.save()
      return redirect('/dashboard/' + str(pk))

  context = {'form':form , 'vname':vname, 'vid':vid}
  return render(request, 'wow/order_form_create.html', context)


@login_required(login_url = 'login')
def updateOrder(request, pk):
  order = RrskRental.objects.get(id=pk)
  form = OrderForm(instance=order)
  # print('ORDER:', order)
  if request.method == 'POST':

    form = OrderForm(request.POST, instance=order)
    if form.is_valid():
      form.save(),order.generate_invoice()
      return redirect('/dashboard/' + str(order.cust.id) )

  context = {'form':form}
  return render(request, 'wow/order_form.html', context)

@login_required(login_url = 'login')
def deleteOrder(request, pk):
  order = RrskRental.objects.get(id=pk)
  if request.method == "POST":
    order.delete()
    return redirect('/dashboard/' + str(order.cust.id))

  context = {'item':order}
  return render(request, 'wow/delete_order.html', context)

@login_required(login_url = 'login')
def payOrder(request,pk,custid):
  custid=int(custid)
  custtype_query=RrskCustomers.objects.raw('select id,cust_type from rrsk_customers where id=%s',[custid])
  custtype=custtype_query[0].cust_type
  if custtype=="I":
    discrate_query=RrskDiscount.objects.raw('select d.id,d.disc_rate from rrsk_customers c join ind_customer ic on c.id=ic.cust_id join rrsk_discount d on ic.disc_id=d.id where c.id=%s', [custid])
    if not discrate_query:
      discrate=0
    else:
      discrate=(discrate_query[0].disc_rate)*100
  elif custtype=="C":
    corpid_query=RrskDiscount.objects.raw('select cc.id,cc.corp_id from rrsk_customers c join corp_customer cc on c.id=cc.cust_id where c.id=%s', [custid])
    corpid=corpid_query[0].corp_id
    print(corpid)
    discrate_query=RrskDiscount.objects.raw('select id,corp_discount from rrsk_corporation where id=%s', [corpid])
    discrate=(discrate_query[0].corp_discount)*100
  discrate=round(discrate,2)
  order = RrskInvoice.objects.get(id=pk)
  cardno = request.POST.get('cardno')
  card_type = request.POST.get('card_type')
  if request.method == 'POST':
    pay = RrskInvoicePayment(pay_amount=order.invoice_amount,pay_method =card_type, card_no = cardno,invoice_no=order)
    pay.save()
    return redirect('/dashboard/' + str(order.rental.cust.id))
  context = {'order': order, 'disc':discrate}
  return render(request, 'wow/pay_form.html',context)

def logoutUser(request):
  logout(request)
  return redirect('/login')



####-------------------------
#%%
def generate_customers(num_customers=200):
  first_names = ['John', 'James', 'Hank', 'Tim', 'Joan','Jane', 'Willy', 'Paul','Sarah', 'Bonnie', 'Will', 'Arthur','Rudy', 'Tom', 'Liza', 'Lizze', 'Rose', 'Lily', 'Amanda']
  last_names = ['Smith', 'Stevens', 'Paulson', 'Cragson', 'Mansfield','Barmaeger', 'Wolls', 'Winner', 'Idleman', 'Shaper', 'Bolt', 'Doad']
  cities = ['New York City', 'Boston', 'Philadelphia', 'Washington DC']

  for i in range(num_customers):
    cust = RrskCustomers(

      # cust_email = '{}@gmail.com'.format(i),
      cust_phone_no = 9999999999 - i,
      cust_type = random.choice(['I', 'C']),
      cust_country = 'USA',
      cust_state = 'NY',
      cust_city = random.choice(cities),
      cust_street = '{} street'.format(i),
      cust_no = '{}'.format(i),
      cust_zip = 10000 + i,
      cust_fname = random.choice(first_names),
      cust_lname = random.choice(last_names))
    cust.save()

def generate_corporations():
  names = ['Visa', 'Mastercard', 'ABC corp', 'Dog and Co', 'Bank of America', 'Jesus Inc.', 'Hello Company', 'Yelp']
  #corp_id = models.DecimalField(primary_key=True, max_digits=32, decimal_places=0)
  for i in range(len(names)):
    corp = RrskCorporation(
       corp_reg_no = 'reg_' + str(i),
       corp_name = names[i],
       corp_discount = random.choice([0,0.1,0.2,0.25,0.205]))
    corp.save()

def generate_corp_customers():
  customers = RrskCustomers.objects.filter(cust_type='C')
  corps = RrskCorporation.objects.all()
  for i in range(len(customers)):
    corp_customer = CorpCustomer(cust=customers[i],
                                 emp_id = i**2,
                                 corp = random.choice(corps))
    corp_customer.save()



def generate_discounts(num=10):
  for i in range(num):
    disc_start_date = datetime.date.today() + datetime.timedelta(days = random.randint(-365, 365))
    disc = RrskDiscount(disc_rate= random.choice([0,0.1,0.2,0.25,0.15]),
                        disc_start_date = disc_start_date,
                        disc_end_date = disc_start_date + datetime.timedelta(days = random.randint(0, 400))
                        )
    disc.save()




def generate_ind_customers():
  customers = RrskCustomers.objects.filter(cust_type='I')
  discounts = RrskDiscount.objects.all()
  for i in range(len(customers)):
    cust = IndCustomer(
      cust = customers[i],
      driver_lisence_no = 'abcd-abcd' + str(i),
      insurance_provider = 'Aflack',
      insurance_policy_no = i,
      disc = random.choice([None, random.choice(discounts)])
      )
    cust.save()


def generate_locations(num=5):
  cities = ['New York City', 'Boston', 'Philadelphia', 'Washington DC']

  for i in range(num):
    loc = RrskLocation(
      loc_phone_no=88888888888 - 5*i**3,
      loc_email = None,
      loc_country = 'USA',
      loc_state = 'New York',
      loc_city = random.choice(cities),
      loc_street = '{} East'.format(2 + i**2),
      loc_no = str(i),
      loc_zip = 10000 + i)
    loc.save()

def generate_vehicle_classes(num=5):
  class_name = ['Compact', 'Sedan', 'SUV', 'Pickup Truck', 'Limousine', 'Sports']
  for i in class_name:
    vclass = RrskVehicleClass(
      class_name = i,
      daily_rate = random.randint(50,600),
      daily_mileage_limit = random.randint(100,400),
      over_mileage_fee = random.randint(1,3))
    vclass.save()


def generate_vehicles(num=70):
  models = ['Land Cruiser', 'Impala', 'Bronco', '911 Carrera', 'MX-5', 'Golf', 'F430 Italia', 'Camry', 'Tahoe', 'Expedition', 'Cayenne', 'CX-30', 'Jetta', 'Enzo', 'Tacoma', 'Camaro']
  makes = ['Toyota', 'Chevrolet', 'Ford', 'Porsche', 'Mazda', 'Volkswagen', 'Ferarri']
  classes = RrskVehicleClass.objects.all()
  locations = RrskLocation.objects.all()
  for i in range(70):
    v = RrskVehicle(
      vin = str(random.randint(1,10000)),
      v_make = random.choice(makes),
      v_model = random.choice(models),
      liscence_plate_no = i,
      available = 'Y',
      v_class = random.choice(classes),
      loc = random.choice(locations))
    v.save()






def generate_rentals(pickup_date = None, dropoff_date = None, v=None, num=400):
  if pickup_date is None and dropoff_date is None and v is None:
    for i in range(num):
      dropoff_location = random.choice(RrskLocation.objects.all())
      v = random.choice(RrskVehicle.objects.filter(loc=dropoff_location))
      v_class = RrskVehicle.objects.get(pk=v.pk).v_class
      pickup_date = datetime.date.today() + datetime.timedelta(days=random.randint(-20, 30))
      dropoff_date = pickup_date + datetime.timedelta(days=random.randint(1, 14))
      start_odometer = random.randint(1,100000)

      if dropoff_date < datetime.date.today():
        end_odometer = start_odometer + random.randint(100, 30000)
      else:
        end_odometer = None
      rental = RrskRental(pickup_date = pickup_date,
                 dropoff_date = dropoff_date,
                 start_odometer = start_odometer,
                 end_odometer = end_odometer,
                 unlimited_mileage = random.choice(['Y', 'N']),
                 cust = random.choice(RrskCustomers.objects.all()),
                 dropoff_location = dropoff_location,
                 v = v,
                 pickup_location = dropoff_location,
                 # v_class = v_class,
                 # loc = v
                 )
      rental.save()


def adminDashboard(request):
  # vehicles, rental loc, invoices paid
    vehicles = random.choices(RrskVehicleClass.objects.raw('SELECT a.id, b.id as vid, b.vin as vin, b.v_make as vmake, b.v_model as vmodel, b.liscence_plate_no as licenseplateno, a.class_name as classname  FROM rrsk_vehicle_class a JOIN rrsk_vehicle b ON a.id = b.v_class_id'),k=30)
    rentalLoc = RrskLocation.objects.raw('SELECT * FROM `rrsk_location`')
    invList = RrskInvoice.objects.raw('SELECT * FROM `rrsk_invoice`')
    print(vehicles)
    # pk_test = int(pk_test)
    
    # past_orders = RrskRental.objects.filter(cust=pk_test,
    #                                         end_odometer__isnull=False)  # .filter(dropoff_date__lte = datetime.date(2020, 12, 17))
    # if len(past_orders) > 0:
    #     past_orders = RrskInvoice.objects.filter(rental__cust__id=pk_test)  #
    #     # past_orders.refresh_from_db()
    
    # pays = []
    # lp = RrskInvoicePayment.objects.all()
    # for it in lp:
    #     print(it.invoice_no.id)
    #     pays.append(int(it.invoice_no.id))
    # pay_pending = RrskInvoice.objects.filter(rental__cust__id=pk_test, id__isnull=False)
    # pay_paid = RrskInvoicePayment.objects.filter(invoice_no_id__rental__cust__id=pk_test)
    # delivered = len(past_orders)
    # curr_orders = RrskRental.objects.filter(cust=pk_test, end_odometer__isnull=True)
    
    # pending = len(curr_orders)
    # total_orders = delivered + pending
    # payment_pending = len(pay_pending)
    # payment_paid = len(pay_paid)
    # payment_due = payment_pending - payment_paid

    rental_cars = RrskVehicle.objects.filter(id__isnull=False)
    rental_locations = RrskLocation.objects.filter(id__isnull=False)
    rental_invoices = RrskInvoice.objects.filter(id__isnull=False)

    total_cars = len(rental_cars)
    total_locations = len(rental_locations)
    total_invoices = len(rental_invoices)
    context = { "vehicles":vehicles,
"rentalLoc":rentalLoc,"invList":invList, 'total_cars': total_cars, 'total_locations': total_locations,  'total_invoices': total_invoices }
    #context = {'past_orders': past_orders, 'curr_orders': curr_orders, 'total_orders': total_orders,
    #'delivered': delivered, 'pending': pending, 'id': pk_test, 'pays': pays
     #}
    return render(request, 'wow/admin_dashboard.html', context)

  
def createRentalLoc(request):
  form = CreateLocForm()
  if request.method == "POST":
    form = CreateLocForm(request.POST)
    loc = form.save()
    loc.loc_country = 'USA'
    loc.save()
    return redirect('/admindashboard/')

  context = {'form':form}
  return render(request, 'wow/rental_loc_create_form.html', context)


def generate_all(request):
  generate_corporations()
  generate_discounts()
  generate_customers()
  
  # generate_corp_customers()
  
  # generate_ind_customers()
  generate_locations()
  generate_vehicle_classes()
  generate_vehicles()
  generate_rentals()











