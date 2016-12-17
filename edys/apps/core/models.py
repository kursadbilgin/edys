# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _


class DateModel(models.Model):
    create_date = models.DateTimeField(verbose_name=_('Create Date'),
                                       auto_now_add=True, editable=False)
    update_Date = models.DateTimeField(verbose_name=_('Update Date'),
                                       auto_now=True, editable=False)

    class Meta:
        abstract = True


class Interest(DateModel):
    name = models.CharField(verbose_name=_('Name'), max_length=75, blank=True,
                            unique=True)

    class Meta:
        verbose_name = _(u'Interest')
        verbose_name_plural = _(u'Interests')

    def __str__(self):
        return self.name
