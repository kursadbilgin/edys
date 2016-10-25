# Django
from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

# Local Django
from core.models import DateModel


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError(_('Users must have email address.'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password):
        if not email:
            raise ValueError(_('Admins must have email address.'))

        user = self.create_user(email,
            first_name=first_name,
            last_name=last_name)

        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name=_('Email'), max_length=255, unique=True)
    first_name = models.CharField(verbose_name=_('First Name'), max_length=50)
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=50)
    affiliation = models.CharField(verbose_name=_('Affiliation'), max_length=100)
    country = models.CharField(verbose_name=_('Country'), max_length=100, blank=True, unique=True)
    is_active = models.BooleanField(verbose_name=_('Active'), default=True)
    is_staff = models.BooleanField(verbose_name=_('Staff'), default=True)
    is_developer = models.BooleanField(verbose_name=_('Developer'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _(u'User')
        verbose_name_plural = _(u'Users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)

        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.get_full_name()
