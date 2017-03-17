from datetime import date
from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from allauth.socialaccount.models import SocialAccount
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=130, unique=True)
    full_name = models.CharField(_('full name'), max_length=130, blank=True)
    email = models.EmailField(_('email id'), max_length=50, blank=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_active = models.BooleanField(_('is_active'), default=True)
    date_joined = models.DateField(_("date_joined"), default=date.today)
    phone_number_verified = models.BooleanField(default=False)
    change_pw = models.BooleanField(default=True)
    phone_number = models.BigIntegerField(blank=True, null=True)
    country_code = models.IntegerField(blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name',]

    class Meta:
        ordering = ('username',)
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_short_name(self):
        return self.username


def save_profile(sender, instance, **kwargs):
    print(instance)
    instance.user.full_name = instance.extra_data['name']
    uid = instance.extra_data['id']
    instance.user.profile_picture = "http://graph.facebook.com/" + uid + "/picture?type=large"
    print("lolalol")
    instance.user.save()

post_save.connect(save_profile, sender=SocialAccount)
