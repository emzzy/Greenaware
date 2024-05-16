from django.db import models
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser

# Create your models here.
class CustomUserAccount(BaseUserManager):
    def create_user(self, email, first_name, last_name, user_role='user', api_key=None, subscription_package=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, user_role=user_role, api_key=api_key, subscription_package=subscription_package, **extra_fields)
        user.set_password(password)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if password is None:
            raise ValueError('The password must be set for superuser.')
        return self.create_user(email, first_name, last_name, password=password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(primary_key=True, max_length=10, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    user_role = models.CharField(max_length=20, default='user')
    api_key = models.CharField(max_length=100, blank=True, null=True)
    subscription_package = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserAccount()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'last_name']

    # Add related_name Attributes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_group' # Unique related name for groups
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions' # Unique related_name for user permission
    )

    def __str__(self):
        return self.email
    
