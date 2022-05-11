from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(CorpCustomer)
admin.site.register(IndCustomer)
admin.site.register(SrkCorporation)
admin.site.register(SrkCustomers)
admin.site.register(SrkDiscount)
admin.site.register(SrkInvoice)
admin.site.register(SrkInvoicePayment)
admin.site.register(SrkLocation)
admin.site.register(SrkRental)
admin.site.register(SrkVehicle)
admin.site.register(SrkVehicleClass)
