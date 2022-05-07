from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(CorpCustomer)
admin.site.register(IndCustomer)
admin.site.register(RrskCorporation)
admin.site.register(RrskCustomers)
admin.site.register(RrskDiscount)
admin.site.register(RrskInvoice)
admin.site.register(RrskInvoicePayment)
admin.site.register(RrskLocation)
admin.site.register(RrskRental)
admin.site.register(RrskVehicle)
admin.site.register(RrskVehicleClass)
