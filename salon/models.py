from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models


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
        return self.salon_name
    
    objects = HairSalonManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['salon_name', 'mobile', 'password', 'licence_number', 'salon_image', 'licence',  'location']

    