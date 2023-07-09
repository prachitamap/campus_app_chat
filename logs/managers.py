from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
'''
class CUserManager(BaseUserManager):
    
    def create_user(self, email, password, first_name, last_name, **extra_fields):
        
        if not email:
            raise ValueError("email is required")
        
        email= self.normalize_email(email)
        user= self.model(email = email, first_name = first_name, last_name = last_name, **extra_fields)
        user.set_password(password)
        user.first_name= first_name
        user.last_name= last_name
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("superuser must have is_staff as true")
        
        return self.create_user(email, password, **extra_fields)
'''
class CUserManager(BaseUserManager):
    
    def create_user(self, email, password,  **extra_fields):
        
        if not email:
            raise ValueError("email is required")
        
        email= self.normalize_email(email)
        user= self.model(email = email, **extra_fields)
        user.set_password(password)
        #user.first_name= first_name
        #user.last_name= last_name
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("superuser must have is_staff as true")
        
        return self.create_user(email, password, **extra_fields)