from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager
from django.core.mail import send_mail
from django.utils.text import slugify



class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """

    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value
 
# Create your models here.
"""This model for creating users"""


class CustomUser(AbstractBaseUser, PermissionsMixin):
   
    name = models.CharField(_("Name"), max_length=150, null=True, blank=True)
    email = LowercaseEmailField(_("Email Address"), unique=True, blank=True)
    password = models.CharField(_("Password"), max_length=200)
    mobile_number = models.CharField(_("Mobile Number"), max_length=12, unique=True)
    
    objects = CustomUserManager()

    is_superuser = models.BooleanField(_("Superuser status"), default=False)
    is_admin = models.BooleanField(_("Admin status"), default=False)
    is_staff = models.BooleanField(_("Staff status"), default=False)
    is_active = models.BooleanField(_("Active status"), default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "User"

    def save(self, *args, **kwargs):
            if len(self.password) < 20:
                self.password = make_password(self.password)
            super().save(*args, **kwargs)

    def __str__(self):
        return self.email
        