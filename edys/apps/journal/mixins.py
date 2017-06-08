# Standard Library
from copy import deepcopy
from functools import partial

# Django
from django.contrib import admin

# Local Django
from journal.forms import ArticleAdminForm
from journal.models import Article


class ArticleAdminMixin(admin.ModelAdmin):
    list_display = ('name', 'title', 'journal')
    filter_horizontal = ('editors', 'assigned_editors', 'reviewers')
    form = ArticleAdminForm
