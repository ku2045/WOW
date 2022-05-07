# Generated by Django 3.1.3 on 2020-12-12 14:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wow', '0004_auto_20201212_0002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rrskrental',
            name='loc',
        ),
        migrations.RemoveField(
            model_name='rrskrental',
            name='v_class',
        ),
        migrations.AlterField(
            model_name='rrskinvoicepayment',
            name='pay_date',
            field=models.DateField(default=datetime.datetime(2020, 12, 12, 14, 51, 49, 564613, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rrskrental',
            name='start_odometer',
            field=models.DecimalField(blank=True, decimal_places=3, default=0, max_digits=9, null=True),
        ),
    ]
