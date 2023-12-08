from django.contrib import admin
from .models import HairSalon, Service, Stylist, TimeSlot

# Register your models here.

admin.site.register(HairSalon)
admin.site.register(Service)
admin.site.register(Stylist)
admin.site.register(TimeSlot)