# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from model_utils import FieldTracker
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
import random
import datetime


class CorpCustomer(models.Model):
    cust = models.OneToOneField('SrkCustomers', models.CASCADE)#, primary_key=True)
    emp_id = models.DecimalField(max_digits=32, decimal_places=0)
    corp = models.ForeignKey('SrkCorporation', models.SET_NULL, null=True)

    class Meta:
        managed = True
        db_table = 'corp_customer'
    def __str__(self):
        return ''.join([self.cust.cust_fname,' ', self.cust.cust_lname])


class IndCustomer(models.Model):
    cust = models.OneToOneField('SrkCustomers', models.CASCADE)#, primary_key=True)
    driver_lisence_no = models.CharField(max_length=12)
    insurance_provider = models.CharField(max_length=64)
    insurance_policy_no = models.DecimalField(max_digits=32, decimal_places=0)
    disc = models.ForeignKey('SrkDiscount', models.SET_NULL, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'ind_customer'
    def __str__(self):
        return ''.join([self.cust.cust_fname,' ', self.cust.cust_lname])


class SrkCorporation(models.Model):
    #corp_id = models.DecimalField(primary_key=True, max_digits=32, decimal_places=0)
    corp_reg_no = models.CharField(max_length=32)
    corp_name = models.CharField(max_length=64)
    corp_discount = models.DecimalField(max_digits=4, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'srk_corporation'
    def __str__(self):
        return self.corp_name

class SrkCustomers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    # print(User.email)
    # cust_email = models.TextField(blank=True, null=True)
    # print(user,cust_email)
    cust_phone_no = models.BigIntegerField(blank=True, null=True)
    cust_type = models.CharField(max_length=1, default='I', blank=True, null=True)
    cust_country = models.CharField(max_length=32, blank=True, null=True)
    cust_state = models.CharField(max_length=32, blank=True, null=True)
    cust_city = models.CharField(max_length=32, blank=True, null=True)
    cust_street = models.CharField(max_length=64, blank=True, null=True)
    cust_no = models.CharField(max_length=32, blank=True, null=True)
    cust_zip = models.IntegerField(blank=True, null=True)
    cust_fname = models.CharField(max_length=32, blank=True, null=True)
    cust_lname = models.CharField(max_length=32, blank=True, null=True)

    def save(self, *args, **kwargs):
        print("hello there",self, self.cust_type)
        super().save(*args, **kwargs)  # Call the "real" save() method.
    
        if (self.cust_type == 'I') and not IndCustomer.objects.filter(cust=self):
            discounts = SrkDiscount.objects.all()
            cust = IndCustomer(
              cust = self,
              driver_lisence_no = 'XX' + str(random.randint(1,10000)),
              insurance_provider = 'Aflack',
              insurance_policy_no = 900,
              disc = random.choice([None, random.choice(discounts)])
              )
            print("saving independent customer")
            cust.save()
        elif (self.cust_type == 'C') and not CorpCustomer.objects.filter(cust=self):
            corps = SrkCorporation.objects.all()
            corp_customer = CorpCustomer(cust=self,
                                         emp_id = random.randint(1,900000000),
                                         corp = random.choice(corps))
            corp_customer.save()

    class Meta:
        managed = True
        db_table = 'srk_customers'
    def __str__(self):
        return ''.join([self.cust_fname,' ', self.cust_lname])

class SrkDiscount(models.Model):
    #disc_id = models.BigIntegerField(primary_key=True)
    disc_rate = models.DecimalField(max_digits=4, decimal_places=4)
    #disc_type = models.CharField(max_length=1)
    disc_start_date = models.DateField()
    disc_end_date = models.DateField()

    def is_valid(self):
      if self.disc_start_date > datetime.date.today():
        return False
      if self.disc_end_date < datetime.date.today():
        return False
      return True

    class Meta:
        managed = True
        db_table = 'srk_discount'




class SrkLocation(models.Model):
    #loc_id = models.BigIntegerField(primary_key=True)
    loc_phone_no = models.BigIntegerField()
    loc_email = models.CharField(max_length=64, blank=True, null=True)
    loc_country = models.CharField(max_length=32)
    loc_state = models.CharField(max_length=32)
    loc_city = models.CharField(max_length=32)
    loc_street = models.CharField(max_length=64)
    loc_no = models.CharField(max_length=32,null=True)
    loc_zip = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'srk_location'
    def __str__(self):
        return ''.join([self.loc_street,' ',self.loc_city,' ',self.loc_country])

class SrkRental(models.Model):
    #rental_id = models.BigIntegerField(primary_key=True)
    pickup_date = models.DateField()
    dropoff_date = models.DateField()
    start_odometer = models.DecimalField(max_digits=9, decimal_places=3, default=0, blank=True, null=True)
    end_odometer = models.DecimalField(max_digits=9, decimal_places=3, blank=True, null=True)
    unlimited_mileage = models.CharField(default='N', max_length=1)
    cust = models.ForeignKey(SrkCustomers, models.SET_NULL, null=True)
    dropoff_location = models.ForeignKey(SrkLocation, models.SET_NULL, null=True, related_name='rental_dropoff_location')
    pickup_location = models.ForeignKey(SrkLocation, models.SET_NULL, null=True, related_name='rental_pickup_location')
    #v_class = models.ForeignKey('SrkVehicle', models.SET_NULL, null=True, related_name='rental_vehicle_class')#, db_column='class_id'  # Field renamed because it was a Python reserved word.
    #loc = models.ForeignKey('SrkVehicle', models.SET_NULL, null=True, related_name='rental_vehicle_location')
    v = models.ForeignKey('SrkVehicle', models.SET_NULL, null=True, related_name='rental_vehicle_id')
    odometer_tracker = FieldTracker(fields=['end_odometer'])



    def generate_invoice(self):
      if not SrkInvoice.objects.filter(rental = self):

        vehicle_class = self.v.v_class #SrkVehicleClass.objects.get(self.v_class)
        days_rented = (self.dropoff_date - self.pickup_date).days
        over_milage = max(0, (self.end_odometer - self.start_odometer) - days_rented*vehicle_class.daily_mileage_limit)

        if self.unlimited_mileage:
         rental_cost = vehicle_class.daily_rate*days_rented
        else:
          rental_cost = (vehicle_class.daily_rate*days_rented
                         + over_milage*vehicle_class.over_mileage_fee)
        if self.cust.cust_type == 'C':
          discount = CorpCustomer.objects.get(cust=self.cust).corp.corp_discount
          #discount =corp_cust.corp.corp_discount
        elif (self.cust.cust_type == 'I'
              and IndCustomer.objects.get(cust=self.cust).disc != None
              and IndCustomer.objects.get(cust=self.cust).disc.is_valid()):
          discount = IndCustomer.objects.get(cust=self.cust).disc.disc_rate
        else:
          discount = 0

        rental_cost = rental_cost*(1 - discount)
        rental_invoice = SrkInvoice(invoice_date=datetime.date.today(),
                                     invoice_amount=rental_cost,
                                     rental = self)
      rental_invoice.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        if (self.end_odometer != self.odometer_tracker.previous('end_odometer')):
          self.generate_invoice()


    class Meta:
        managed = True
        db_table = 'srk_rental'
    def __str__(self):
        if self.cust != None:
          return ''.join([str(self.id),' ',self.cust.cust_fname, ' ', self.cust.cust_lname])
        else:
          return ''.join([str(self.id), '<UNKNOWN>'])
class SrkVehicle(models.Model):
    #v_id = models.DecimalField(max_digits=32, decimal_places=0, primary_key=True)
    vin = models.CharField(max_length=17)
    v_make = models.CharField(max_length=20)
    v_model = models.CharField(max_length=32)
    liscence_plate_no = models.CharField(max_length=12)
    available = models.CharField(max_length=1)
    v_class = models.ForeignKey('SrkVehicleClass', models.CASCADE)#, db_column='class_id')  # Field renamed because it was a Python reserved word.
    loc = models.ForeignKey(SrkLocation, models.SET_NULL, null=True)

    class Meta:
        managed = True
        db_table = 'srk_vehicle'
        unique_together = (('v_class', 'loc', 'id'),)
    def __str__(self):
        return ''.join([str(self.id), ' ', self.v_make, ' ', self.v_model , ' -- ',  str(self.loc)])

class SrkVehicleClass(models.Model):
    #class_id = models.BigIntegerField(primary_key=True)
    class_name = models.CharField(max_length=32)
    daily_rate = models.DecimalField(max_digits=7, decimal_places=2)
    daily_mileage_limit = models.IntegerField()
    over_mileage_fee = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        managed = True
        db_table = 'srk_vehicle_class'

    def __str__(self):
        return self.class_name


class SrkInvoice(models.Model):
    #invoice_no = models.BigIntegerField(primary_key=True)
    invoice_date = models.DateField()
    invoice_amount = models.DecimalField(max_digits=9, decimal_places=2)
    rental = models.OneToOneField('SrkRental', models.SET_NULL, null=True)

    class Meta:
        managed = True
        db_table = 'srk_invoice'


class SrkInvoicePayment(models.Model):
    #pay_id = models.BigIntegerField(primary_key=True)
    pay_amount = models.DecimalField(max_digits=9, decimal_places=2)
    pay_date = models.DateField(default=now())
    pay_method = models.CharField(choices=[('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('Gift Card', 'Gift Card')], default = 'Credit Card', max_length=16)
    card_no = models.DecimalField(max_digits=19, decimal_places=0)
    invoice_no = models.ForeignKey(SrkInvoice, models.SET_NULL, null=True)#, db_column='invoice_no')

    class Meta:
        managed = True
        db_table = 'srk_invoice_payment'

#@receiver(post_save, sender=User)
#def update_SrkCustomers_signal(sender, instance, created, **kwargs):
#    if created:
#        SrkCustomers.objects.create(user=instance, cust_fname=instance.first_name, cust_lname=instance.last_name, cust_email=instance.email)
#
#@receiver(post_save, sender=User)
#def save_user_profile(sender, instance, **kwargs):
#    instance.profile.save()