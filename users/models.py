from datetime import date
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=130, unique=True)
    full_name = models.CharField(_('full name'), max_length=130, blank=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_active = models.BooleanField(_('is_active'), default=True)
    date_joined = models.DateField(_("date_joined"), default=date.today)
    phone_number_verified = models.BooleanField(default=False)
    change_pw = models.BooleanField(default=True)
    phone_number = models.BigIntegerField(unique=True)
    country_code = models.IntegerField()

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'phone_number', 'country_code']

    class Meta:
        ordering = ('username',)
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_short_name(self):
        """
        Returns the display name.
        If full name is present then return full name as display name
        else return username.
        """
        if self.full_name != '':
            return self.full_name
        else:
            return self.username
