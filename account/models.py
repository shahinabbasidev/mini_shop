from django.utils import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        """
        Creates and saves a User with the given phone and password.
        """
        if not phone:
            raise ValueError("Users must have a phone number")

        user = self.model(
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given phone and password.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        blank=True,
        null=True,
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=30, verbose_name="full name", blank=True, null=True)
    phone = models.CharField(max_length=13, verbose_name="phone number", unique=True, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name="date joined", default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Otp(models.Model):
    token = models.CharField(max_length=200,null=True,blank=True)
    phone = models.CharField(max_length=13)
    code = models.SmallIntegerField(null=True, blank=True)
    expires = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.phone
