from datetime import date

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """User model"""
    email = models.EmailField(unique=True, db_index=True, verbose_name='Email Address')
    first_name = models.CharField(max_length=40, verbose_name='First name')
    last_name = models.CharField(max_length=40, verbose_name='Last name')
    birth_date = models.DateField(default=date.today, verbose_name='Birth date')
    bio = models.TextField(verbose_name='Bio')
    is_verified = models.BooleanField(default=False,
                                      help_text='Determines whether the user is verified.',
                                      verbose_name='Is verified')
    is_active = models.BooleanField(default=False,
                                    help_text='Designates whether this user should be treated as active. ''Unselect '
                                              'this instead of deleting accounts.',
                                    verbose_name='Is active')
    is_staff = models.BooleanField(default=False,
                                   help_text='Designates whether the user can log into this admin site.',
                                   verbose_name='Is staff')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Registration date')
    last_visit = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
