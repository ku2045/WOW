# Generated by Django 3.1.3 on 2020-12-12 04:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='srkinvoicepayment',
            name='pay_date',
            field=models.DateField(default=datetime.datetime(2020, 12, 12, 4, 41, 10, 875857, tzinfo=utc)),
        ),
    ]
