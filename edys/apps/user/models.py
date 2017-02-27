# Django
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

# Local Django
from core.models import DateModel
from core.variables import (
    USER_TYPES,
    USER_DEFAULT, USER_EDITOR,
    USER_ASSIGNEDEDITOR, USER_REVIEWER
)



class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError(_('Users must have email address.'))

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name
        )

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
    user_type = models.PositiveSmallIntegerField(verbose_name=_('User Type'),
                                                 choices=USER_TYPES,
                                                 default=USER_DEFAULT)
    email = models.EmailField(verbose_name=_('Email'), max_length=255,
                              unique=True)
    first_name = models.CharField(verbose_name=_('First Name'), max_length=50)
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=50)
    affiliation = models.CharField(verbose_name=_('Affiliation'),
                                   max_length=100)
    country = models.CharField(verbose_name=_('Country'), max_length=100,
                                blank=True, null=True)
    is_active = models.BooleanField(verbose_name=_('Active'), default=True)
    is_staff = models.BooleanField(verbose_name=_('Staff'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _(u'User')
        verbose_name_plural = _(u'Users')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)

        return full_name.strip()

    def get_short_name(self):
        return self.first_name


class Interest(DateModel):
    name = models.CharField(verbose_name=_('Name'), max_length=75, blank=True,
                            unique=True)
    user = models.ForeignKey(verbose_name=('User'), to=User)

    class Meta:
        verbose_name = _(u'Interest')
        verbose_name_plural = _(u'Interests')

    def __str__(self):
        return self.name


# Proxy User Model -> Default
class UserDefaultModelManager(models.Manager):
    def get_queryset(self):
        return super(UserDefaultModelManager, self).get_queryset().filter(user_type=USER_DEFAULT)


class UserDefault(User):
    objects = UserDefaultModelManager()

    class Meta:
        proxy = True
        verbose_name = _(u'User')
        verbose_name_plural = _(u'Users')

    def save(self, *args, **kwargs):
        self.user_type = USER_DEFAULT
        super(UserDefault, self).save(*args, **kwargs)


# Proxy User Model -> Editor
class UserEditorModelManager(models.Manager):
    def get_queryset(self):
        return super(UserEditorModelManager, self).get_queryset().filter(user_type=USER_EDITOR)


class UserEditor(User):
    objects = UserEditorModelManager()

    class Meta:
        proxy = True
        verbose_name = _(u'Editor')
        verbose_name_plural = _(u'Editors')

    def save(self, *args, **kwargs):
        self.user_type = USER_EDITOR
        super(UserEditor, self).save(*args, **kwargs)


# Proxy User Model -> Assigned Editor
class UserAssignedEditorModelManager(models.Manager):
    def get_queryset(self):
        return super(UserAssignedEditorModelManager, self).get_queryset().filter(user_type=USER_ASSIGNEDEDITOR)


class UserAssignedEditor(User):
    objects = UserAssignedEditorModelManager()

    class Meta:
        proxy = True
        verbose_name = _(u'Assigned Editor')
        verbose_name_plural = _(u'Assigned Editors')

    def save(self, *args, **kwargs):
        self.user_type = USER_ASSIGNEDEDITOR
        super(UserAssignedEditor, self).save(*args, **kwargs)


# Proxy User Model -> Reviewer
class UserReviewerModelManager(models.Manager):
    def get_queryset(self):
        return super(UserReviewerModelManager, self).get_queryset().filter(user_type=USER_REVIEWER)


class UserReviewer(User):
    objects = UserReviewerModelManager()

    class Meta:
        proxy = True
        verbose_name = _(u'Reviewer')
        verbose_name_plural = _(u'Reviewers')

    def save(self, *args, **kwargs):
        self.user_type = USER_REVIEWER
        super(UserReviewer, self).save(*args, **kwargs)
