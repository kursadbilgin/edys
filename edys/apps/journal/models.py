# Standart Library
import os

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Local Django
from user.models import User
from core.models import DateModel


class Journal(DateModel):
    user = models.ForeignKey(verbose_name=_('User'), to=User)
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    content = models.CharField(verbose_name=_('Content'), max_length=200)

    class Meta:
        verbose_name=_(u'Journal')
        verbose_name_plural=_(u'Journals')

    def __str__(self):
        return self.name

class Period(DateModel):
    period = models.CharField(verbose_name=_('Period'), max_length=100)
    user = models.ForeignKey(verbose_name=_('User'), to=User)
    journal = models.ForeignKey(verbose_name=_('Journal'), to=Journal)

    class Meta:
        verbose_name=_(u'Period')
        verbose_name_plural=_(u'Periods')

    def __str__(self):
        return self.period


class Article(DateModel):
    user = models.ForeignKey(verbose_name=_('User'), to=User)
    journal = models.ForeignKey(verbose_name=_('Journal'), to=Journal)
    period = models.ForeignKey(verbose_name=_('Period'), to=Period,
                                related_name='article')
    title = models.CharField(verbose_name=_('Title'), max_length=100)
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    abstract = models.TextField(verbose_name=_('Abstract'), max_length=300)

    class Meta:
        verbose_name = _(u'Article')
        verbose_name_plural = _(u'Article')

    def __str__(self):
        return self.name


def set_upload_document_path(instance, filename):
    return os.path.join("article_%d" % instance.article.id, filename)


class ArticleDocument(DateModel):
    description = models.CharField(verbose_name=_('Description'), max_length=100,
                                   null=True)
    document = models.FileField(verbose_name=_('Document'),
                                upload_to=set_upload_document_path)
    article = models.ForeignKey(verbose_name=_('Article'), to=Article,
                                related_name='article_documents')

    class Meta:
        verbose_name = _(u'Article Document')
        verbose_name_plural = _(u'Article Documents')

    def __str__(self):
        return self.description
