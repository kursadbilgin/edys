# Standart Library
import os

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Local Django
from core.models import DateModel

###     Title     ###

class Title(DateModel):
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    abstract = models.TextField(verbose_name=_('Abstract'), max_length=300)

    class Meta:
        verbose_name=_(u'Title')
        verbose_name_plural=_(u'Titles')

    def __str__(self):
        return self.name

####################

###     Journal     ###

class Journal(DateModel):
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    period = models.CharField(verbose_name=_('Period'), max_length=100)
    content = models.CharField(verbose_name=_('Content'), max_length=200)
    titles = models.ManyToManyField(verbose_name=_('Titles'), to=Title)

    class Meta:
        verbose_name=_(u'Journal')
        verbose_name_plural=_(u'Journals')

    def __str__(self):
        return self.name

    def get_titles(self):
        return "\n".join([str(titles) for titles in self.titles.all()])

####################

###     Article     ###

class Article(DateModel):
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    titles = models.ManyToManyField(verbose_name=_('Titles'), to=Title)
    abstract = models.TextField(verbose_name=_('Abstract'), max_length=300)

    class Meta:
        verbose_name = _(u'Article')
        verbose_name_plural = _(u'Article')

    def __str__(self):
        return self.name

    def get_titles(self):
        return "\n".join([str(titles) for titles in self.titles.all()])

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
