from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """User model"""
    birth_date = models.DateField(default=date.today, verbose_name='Birth date')
    bio = models.TextField(verbose_name='Bio')
    is_verified = models.BooleanField(default=False,
                                      help_text='Determines whether the user is verified.',
                                      verbose_name='Is Verified')

    def __str__(self):
        return self.username
