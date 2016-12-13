# Standart Library
import os

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Local Django
from user.models import User
from core.models import DateModel

###     Journal     ###

class Journal(DateModel):
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    period = models.CharField(verbose_name=_('Period'), max_length=100)
    content = models.CharField(verbose_name=_('Content'), max_length=200)

    class Meta:
        verbose_name=_(u'Journal')
        verbose_name_plural=_(u'Journals')

    def __str__(self):
        return self.name

####################

###     Article     ###

class Article(DateModel):
    journal = models.ForeignKey(verbose_name=_('Journal'), to=Journal, related_name='article')
    title = models.CharField(verbose_name=_('Title'), max_length=100)
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    abstract = models.TextField(verbose_name=_('Abstract'), max_length=300)

    class Meta:
        verbose_name = _(u'Article')
        verbose_name_plural = _(u'Article')

    def __str__(self):
        return self.name

####################

def set_upload_document_path(instance, filename):
    return os.path.join(
      "article_%d" % instance.article.id, filename)

####################

###     Article Document     ###

class ArticleDocument(DateModel):
    description = models.CharField(verbose_name=_('Description'), max_length=100, null=True)
    document = models.FileField(verbose_name=_('Document'), upload_to=set_upload_document_path)
    article = models.ForeignKey(verbose_name=_('Article'), to=Article, related_name='article_documents')

    class Meta:
        verbose_name = _(u'Article Document')
        verbose_name_plural = _(u'Article Documents')

    def __str__(self):
        return self.description

####################
