from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from . managers import CUserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.

class CUser(AbstractUser, PermissionsMixin):
    #id = models.AutoField()
    username = models.CharField(max_length = 50 , unique = True)
    email = models.EmailField(_('email address') , unique = True)
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length= 20)
    branch = models.CharField(max_length = 50 , default = '')
    year = models.IntegerField(default=0)  
    mobile = models.CharField(max_length=10, default='')
    secret_key = models.CharField(max_length=256 , null=True, blank=True)
    expiry_time = models.DateTimeField(blank=True , null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CUserManager()
    
    def __str__(self):
        return self.email