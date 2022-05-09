# Generated by Django 3.1.3 on 2020-12-12 04:31

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RrskCorporation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corp_reg_no', models.CharField(max_length=32)),
                ('corp_name', models.CharField(max_length=64)),
                ('corp_discount', models.DecimalField(blank=True, decimal_places=4, max_digits=4, null=True)),
            ],
            options={
                'db_table': 'rrsk_corporation',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RrskCustomers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cust_email', models.CharField(blank=True, max_length=64, null=True)),
                ('cust_phone_no', models.BigIntegerField(blank=True, null=True)),
                ('cust_type', models.CharField(blank=True, default='I', max_length=1, null=True)),
                ('cust_country', models.CharField(blank=True, max_length=32, null=True)),
                ('cust_state', models.CharField(blank=True, max_length=32, null=True)),
                ('cust_city', models.CharField(blank=True, max_length=32, null=True)),
                ('cust_street', models.CharField(blank=True, max_length=64, null=True)),
                ('cust_no', models.CharField(blank=True, max_length=32, null=True)),
                ('cust_zip', models.IntegerField(blank=True, null=True)),
                ('cust_fname', models.CharField(blank=True, max_length=32, null=True)),
                ('cust_lname', models.CharField(blank=True, max_length=32, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'rrsk_customers',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RrskDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disc_rate', models.DecimalField(decimal_places=4, max_digits=4)),
                ('disc_start_date', models.DateField()),
                ('disc_end_date', models.DateField()),
            ],
            options={
                'db_table': 'rrsk_discount',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RrskInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_date', models.DateField()),
                ('invoice_amount', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
            options={
                'db_table': 'rrsk_invoice',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RrskLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loc_phone_no', models.BigIntegerField()),
                ('loc_email', models.CharField(blank=True, max_length=64, null=True)),
                ('loc_country', models.CharField(max_length=32)),
                ('loc_state', models.CharField(max_length=32)),
                ('loc_city', models.CharField(max_length=32)),
                ('loc_street', models.CharField(max_length=64)),
                ('loc_no', models.CharField(max_length=32)),
                ('loc_zip', models.IntegerField()),
            ],
            options={
                'db_table': 'rrsk_location',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RrskVehicleClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=32)),
                ('daily_rate', models.DecimalField(decimal_places=2, max_digits=7)),
                ('daily_mileage_limit', models.IntegerField()),
                ('over_mileage_fee', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'db_table': 'rrsk_vehicle_class',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RrskVehicle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vin', models.CharField(max_length=17)),
                ('v_make', models.CharField(max_length=20)),
                ('v_model', models.CharField(max_length=32)),
                ('liscence_plate_no', models.CharField(max_length=12)),
                ('available', models.CharField(max_length=1)),
                ('loc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wow.rrsklocation')),
                ('v_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wow.rrskvehicleclass')),
            ],
            options={
                'db_table': 'rrsk_vehicle',
                'managed': True,
                'unique_together': {('v_class', 'loc', 'id')},
            },
        ),
        migrations.CreateModel(
            name='RrskRental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pickup_date', models.DateField()),
                ('dropoff_date', models.DateField()),
                ('start_odometer', models.DecimalField(blank=True, decimal_places=3, max_digits=9, null=True)),
                ('end_odometer', models.DecimalField(blank=True, decimal_places=3, max_digits=9, null=True)),
                ('unlimited_mileage', models.CharField(default='N', max_length=1)),
                ('cust', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wow.rrskcustomers')),
                ('dropoff_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rental_dropoff_location', to='wow.rrsklocation')),
                ('loc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rental_vehicle_location', to='wow.rrskvehicle')),
                ('pickup_location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rental_pickup_location', to='wow.rrsklocation')),
                ('v', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rental_vehicle_id', to='wow.rrskvehicle')),
                ('v_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rental_vehicle_class', to='wow.rrskvehicle')),
            ],
            options={
                'db_table': 'rrsk_rental',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RrskInvoicePayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('pay_date', models.DateField(default=datetime.datetime(2020, 12, 12, 4, 31, 12, 627290, tzinfo=utc))),
                ('pay_method', models.CharField(choices=[('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('Gift Card', 'Gift Card')], default='Credit Card', max_length=16)),
                ('card_no', models.DecimalField(decimal_places=0, max_digits=19)),
                ('invoice_no', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wow.rrskinvoice')),
            ],
            options={
                'db_table': 'rrsk_invoice_payment',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='rrskinvoice',
            name='rental',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wow.rrskrental'),
        ),
        migrations.CreateModel(
            name='IndCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver_lisence_no', models.CharField(max_length=12)),
                ('insurance_provider', models.CharField(max_length=64)),
                ('insurance_policy_no', models.DecimalField(decimal_places=0, max_digits=32)),
                ('cust', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wow.rrskcustomers')),
                ('disc', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wow.rrskdiscount')),
            ],
            options={
                'db_table': 'ind_customer',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CorpCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.DecimalField(decimal_places=0, max_digits=32)),
                ('corp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wow.rrskcorporation')),
                ('cust', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wow.rrskcustomers')),
            ],
            options={
                'db_table': 'corp_customer',
                'managed': True,
            },
        ),
    ]
