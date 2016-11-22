# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Journal(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=150)
    period = models.CharField(verbose_name=_('Period'), max_length=100)
    content = models.CharField(verbose_name=_('Content'), max_length=200)


    class Meta():
        verbose_name=_(u'Journal')
        verbose_name_plural=_(u'Journals')

    def __str__(self):
        self.name
