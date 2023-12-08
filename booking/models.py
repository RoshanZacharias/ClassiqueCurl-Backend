from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from salon.models import Service, Stylist, TimeSlot, HairSalon

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Create and return a regular user with an email and password.
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Create and return a superuser with an email and password.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    

    
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=20)
    is_blocked = models.BooleanField(default=False)

    # Add any additional fields you need
    groups = models.ManyToManyField(Group, blank=True, related_name='custom_user_groups', related_query_name='custom_user')
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='custom_user_permissions',
        related_query_name='custom_user_permission'
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile', 'password']





class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100, null=True)
    user_email = models.CharField(max_length=100, null=True)
    salon = models.ForeignKey(HairSalon, on_delete=models.CASCADE, null=True)
    salon_name = models.CharField(max_length=100, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    stylist = models.ForeignKey(Stylist, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_booked = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user} - {self.service} - {self.date}"
    
