from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
import time
import uuid


# Create your models here.


class HairSalonManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Create and return a regular user with an email and password.
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    


class HairSalon(AbstractBaseUser, PermissionsMixin):
    salon_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    licence = models.ImageField(upload_to='licences/', default='default_license.jpg')  
    salon_image = models.ImageField(upload_to='salonImages/', default='default_image.jpg')
    licence_number = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.salon_name},  id={self.id}'
    
    objects = HairSalonManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['salon_name', 'mobile', 'password', 'licence_number', 'salon_image', 'licence',  'location']

    


class Service(models.Model):
    service_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    salon = models.ForeignKey(HairSalon, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.service_name


class Stylist(models.Model):
    stylist_name = models.CharField(max_length=100)
    stylist_image = models.ImageField(upload_to='stylistImages/', default='default_image.jpg')
    salon = models.ForeignKey(HairSalon, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.stylist_name
    



class TimeSlot(models.Model):
    day_choices = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    day = models.CharField(max_length=15, choices=day_choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    salon = models.ForeignKey(HairSalon, on_delete=models.CASCADE, null=True)
    is_booked = models.BooleanField(default=False)


    def __str__(self):
        return self.day
    
    