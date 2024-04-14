from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email field should be set')
        if not password:
            raise ValueError('Password field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class Role(models.Model):
    USER_ROLE = 'user'
    CREATOR_ROLE = 'creator'

    ROLE_CHOICES = (
        (USER_ROLE, 'User'),
        (CREATOR_ROLE, 'Creator'),
    )

    name = models.CharField(max_length=20, choices=ROLE_CHOICES, default=USER_ROLE)

    def __str__(self):
        return self.name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, default=None)
    first_name = models.CharField(max_length=200, blank=True, null=True, default=None)
    last_name = models.CharField(max_length=200, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_notification_required = models.BooleanField(default=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


