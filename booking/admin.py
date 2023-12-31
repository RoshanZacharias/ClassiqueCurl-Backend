from django.contrib import admin
from .models import CustomUser, Appointment, Order, ReimbursedAmount, Wallet, Notification


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Appointment)
admin.site.register(Order)
admin.site.register(ReimbursedAmount)
admin.site.register(Wallet)
admin.site.register(Notification)