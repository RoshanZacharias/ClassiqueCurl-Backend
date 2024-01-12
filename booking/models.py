from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from salon.models import Service, Stylist, TimeSlot, HairSalon
from django.contrib.auth import get_user_model


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
    password = models.CharField(max_length=128)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
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
        
    

class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)





class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    user_name = models.CharField(max_length=100, null=True)
    user_email = models.CharField(max_length=100, null=True)
    salon = models.ForeignKey(HairSalon, on_delete=models.CASCADE, null=True)
    salon_name = models.CharField(max_length=100, null=True)
    order_service = models.CharField(max_length=100)
    order_stylist = models.CharField(max_length=100)
    order_amount = models.CharField(max_length=25)
    order_payment_id = models.CharField(max_length=100)
    isPaid = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now=True)
    time_slot_date = models.DateField(null=True)
    time_slot_day = models.CharField(max_length=100, null=True)  
    time_slot_start_time = models.TimeField(null=True) 
    time_slot_end_time = models.TimeField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    convenience_fee = models.DecimalField(max_digits=10, decimal_places=2, default=25.00)

    def __str__(self):
        return self.order_service
    




class ReimbursedAmount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user} - {self.order} - ₹{self.amount}"






class Notification(models.Model):
   NOTIFICATION_TYPES = [
        ('booked', 'New Booked'),
        ('pending', 'New Pending'),
        ('completed', 'New Completed'),
        ('cancelled', 'New Cancelled'),
        
    ]
   
   RECEIVER_TYPE = [
       ('customuser','CUSTOMUSER'),
       ('salonuser', 'SALONUSER'),
   ]
   
   
   
   customer = models.ForeignKey(CustomUser, related_name="notification_to", on_delete=models.CASCADE, null=True)
   salonUser = models.ForeignKey(HairSalon, related_name="notification_from", on_delete=models.CASCADE, null=True)
   receiver_type = models.CharField(choices=RECEIVER_TYPE, max_length=20, null=True)
   message = models.CharField(max_length=20, null=True)
   notification_type = models.CharField(choices=NOTIFICATION_TYPES, max_length=20)
   created = models.DateTimeField(auto_now_add=True)
   is_seen = models.BooleanField(default=False)
   
   def _str_(self):
        return f"{self.from_user} sent a {self.notification_type} notification to {self.to_user}"


