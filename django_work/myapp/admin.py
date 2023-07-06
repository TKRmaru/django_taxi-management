from django.contrib import admin
from .models import CarInformation, CustomerInformation, PlaceInformation, SalesRecord

admin.site.register(CarInformation)
admin.site.register(CustomerInformation)
admin.site.register(PlaceInformation)
admin.site.register(SalesRecord)
