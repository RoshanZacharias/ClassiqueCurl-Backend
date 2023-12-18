from django.contrib import admin
from .models import CustomUser, Appointment, Order, ReimbursedAmount


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Appointment)
admin.site.register(Order)
admin.site.register(ReimbursedAmount)