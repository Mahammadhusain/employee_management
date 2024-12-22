from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    ]
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_of_joining = models.DateField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    supervised_by = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='supervised_employees'
    )

    REQUIRED_FIELDS = ['email', 'name', 'date_of_joining']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

