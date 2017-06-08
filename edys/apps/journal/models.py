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
    max_file_size = models.PositiveSmallIntegerField(
        verbose_name=('Maximum File Size'), null=True
    )
    editors = models.ManyToManyField(
        verbose_name=_('Editors'), to=User, related_name='journal_editors',
        limit_choices_to={'is_superuser': False}
    )
    assigned_editors = models.ManyToManyField(
        verbose_name=_('Assigned Editors'), to=User,
        related_name='journal_assigned_editors',
        limit_choices_to={'is_superuser': False}
    )

    class Meta:
        verbose_name=_(u'Journal')
        verbose_name_plural=_(u'Journals')

    def __str__(self):
        return self.name


class Period(DateModel):
    period = models.PositiveSmallIntegerField(verbose_name=_('Period'))
    user = models.ForeignKey(verbose_name=_('User'), to=User)
    journal = models.ForeignKey(verbose_name=_('Journal'), to=Journal)

    class Meta:
        verbose_name=_(u'Period')
        verbose_name_plural=_(u'Periods')

    def __str__(self):
        return str(self.period)


class Article(DateModel):
    user = models.ForeignKey(verbose_name=_('User'), to=User)
    journal = models.ForeignKey(verbose_name=_('Journal'), to=Journal)
    title = models.CharField(verbose_name=_('Title'), max_length=100)
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    abstract = models.TextField(verbose_name=_('Abstract'))
    editors = models.ManyToManyField(
        verbose_name=_('Editors'), to=User, related_name='article_editors',
        limit_choices_to={'is_superuser': False}
    )
    assigned_editors = models.ManyToManyField(
        verbose_name=_('Assigned Editors'), to=User,
        related_name='article_assigned_editors',
        limit_choices_to={'is_superuser': False},
        null=True, blank=True
    )
    reviewers = models.ManyToManyField(
        verbose_name=_('Reviewer'), to=User,
        related_name='article_reviewers',
        limit_choices_to={'is_superuser': False},
        null=True, blank=True
    )

    class Meta:
        verbose_name = _(u'Article')
        verbose_name_plural = _(u'Article')

    def __str__(self):
        return self.name


# Proxy Article Model 1
class ArticleProxyModel(models.Manager):
    def get_queryset(self):
        return super(ArticleProxyModel, self).get_queryset()


class ArticleProxy(Article):
    objects = ArticleProxyModel()

    class Meta:
        proxy = True
        verbose_name = _(u'Article I have added')
        verbose_name_plural = _(u'Articles I have added')


# Proxy Article Model 2
class ArticleProxyModelT(models.Manager):
    def get_queryset(self):
        return super(ArticleProxyModelT, self).get_queryset()


class ArticleProxyT(Article):
    objects = ArticleProxyModelT()

    class Meta:
        proxy = True
        verbose_name = _(u'Assigned Article')
        verbose_name_plural = _(u'Assigned Articles')


def set_upload_document_path(instance, filename):
    return os.path.join("article_%d" % instance.article.id, filename)


class ArticleDocument(DateModel):
    description = models.CharField(
        verbose_name=_('Description'), max_length=100,null=True
    )
    document = models.FileField(
        verbose_name=_('Document'),upload_to=set_upload_document_path
    )
    article = models.ForeignKey(verbose_name=_('Article'), to=Article)

    class Meta:
        verbose_name = _(u'Article Document')
        verbose_name_plural = _(u'Article Documents')

    def __str__(self):
        return self.description

    def get_size(self):
        return self.document._get_size()

    get_size.short_description =  _('Size')
