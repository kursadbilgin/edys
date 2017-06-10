# Standard Library
from copy import deepcopy
from functools import partial

# Django
from django.db.models import Q
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row

# Local Django
from user.models import User
from journal.forms import (
    ArticleAdminForm, ArticleProxyTAdminForm, ArticleDocumentAdminForm
)
from journal.mixins import ArticleAdminMixin
from journal.models import (
    Journal, Period, Article, ArticleProxy, ArticleProxyT, ArticleDocument
)
from core.variables import GROUP_ADMIN, GROUP_DEFAULT


@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    ctx = original_submit_row(context)
    ctx.update({
        'show_save_and_add_another': context.get('show_save_and_add_another', ctx['show_save_and_add_another']),
        'show_save_and_continue': context.get('show_save_and_continue', ctx['show_save_and_continue']),
        'show_save': context.get('show_save', ctx['show_save'])
        })
    return ctx


class ArticleDocumentInline(admin.StackedInline):
    model = ArticleDocument
    extra = 0
    min_num = 1
    verbose_name = _('Document')
    verbose_name_plural = _('Documents')
    form = ArticleDocumentAdminForm


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)
    filter_horizontal = ('editors', 'assigned_editors')

    def get_fields(self, request, *args, **kwargs):
        fields = super(JournalAdmin, self). get_fields(request, *args, **kwargs)

        exclude_fields = []
        group_names = [group.name for group in request.user.groups.all()]
        if not request.user.is_superuser:
            exclude_fields.append('user',)
            if not GROUP_ADMIN in group_names:
                exclude_fields.append('editors')
                exclude_fields.append('assigned_editors')

        return [field for field in fields if field not in exclude_fields]

    def get_queryset(self, request):
        qs = super(JournalAdmin, self).get_queryset(request)

        group_names = [group.name for group in request.user.groups.all()]
        if not request.user.is_superuser and not GROUP_DEFAULT in group_names:
            qs = qs.filter(user=request.user.id)

        return qs

    def has_add_permission(self, request):
        group_names = [group.name for group in request.user.groups.all()]
        if request.user.is_superuser or GROUP_ADMIN in group_names:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        group_names = [group.name for group in request.user.groups.all()]
        if request.user.is_superuser or GROUP_ADMIN in group_names:
            return True
        else:
            return False

    def get_actions(self, request):
        actions = super(JournalAdmin, self).get_actions(request)

        group_names = [group.name for group in request.user.groups.all()]
        if not request.user.is_superuser and not GROUP_ADMIN in group_names:
            del actions['delete_selected']

        return actions

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user

        obj.save()

    def get_readonly_fields(self, request, obj=None):
        actions = super(JournalAdmin, self). get_actions(request)

        group_names = [group.name for group in request.user.groups.all()]
        if request.user.is_superuser or GROUP_ADMIN in group_names:
            return self.readonly_fields
        else:
            readonly_fields = ['editors', 'assigned_editors', 'max_file_size', 'name', 'content']
            return readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        group_names = [group.name for group in request.user.groups.all()]
        if not request.user.is_superuser and not GROUP_ADMIN in group_names:
            extra_context = extra_context or {}
            extra_context['show_save_and_add_another'] = False
            extra_context['show_save_and_continue'] = False
            extra_context['show_save'] = False
        return super(JournalAdmin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('period', 'journal')
    ordering = ('period',)

    def get_fields(self, request, *args, **kwargs):
        fields = super(PeriodAdmin, self). get_fields(request, *args, **kwargs)

        exclude_fields = []
        if not request.user.is_superuser:
            exclude_fields.append('user')

        return [field for field in fields if field not in exclude_fields]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "journal" and not request.user.is_superuser:
            kwargs["queryset"] = Journal.objects.filter(user=request.user)

        return super(PeriodAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(PeriodAdmin, self).get_queryset(request)

        if request.user.is_superuser:
            qs = qs.filter(journal__period__user=request.user.id)

        return qs

    def has_add_permission(self, request):
        group_names = [group.name for group in request.user.groups.all()]
        if request.user.is_superuser or GROUP_ADMIN in group_names:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        group_names = [group.name for group in request.user.groups.all()]
        if request.user.is_superuser or GROUP_ADMIN in group_names:
            return True
        else:
            return False

    def get_actions(self, request):
        actions = super(PeriodAdmin, self).get_actions(request)

        group_names = [group.name for group in request.user.groups.all()]
        if not request.user.is_superuser and not GROUP_ADMIN in group_names:
            del actions['delete_selected']

        return actions

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user

        obj.save()

    def get_readonly_fields(self, request, obj=None):
        actions = super(PeriodAdmin, self). get_actions(request)

        group_names = [group.name for group in request.user.groups.all()]
        if request.user.is_superuser or GROUP_ADMIN in group_names:
            return self.readonly_fields
        else:
            readonly_fields = ['period', 'journal']
            return readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        group_names = [group.name for group in request.user.groups.all()]
        if not request.user.is_superuser and not GROUP_ADMIN in group_names:
            extra_context = extra_context or {}
            extra_context['show_save_and_add_another'] = False
            extra_context['show_save_and_continue'] = False
            extra_context['show_save'] = False
        return super(PeriodAdmin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)


@admin.register(Article)
class ArticleAdmin(ArticleAdminMixin):
    inlines = (ArticleDocumentInline,)

    def get_fields(self, request, *args, **kwargs):
        fields = super(ArticleAdmin, self). get_fields(request, *args, **kwargs)

        exclude_fields = []
        if not request.user.is_superuser:
            exclude_fields.append('user')
            exclude_fields.append('journal')
            exclude_fields.append('editors')
            exclude_fields.append('assigned_editors')
            exclude_fields.append('reviewers')

        return [field for field in fields if field not in exclude_fields]

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)

        return qs

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.user = request.user

            try:
                journal = Journal.objects.get(id=request.GET.get('journal'))
                obj.journal = journal
            except Journal.DoesNotExist:
                pass

        obj.save()


@admin.register(ArticleProxy)
class ArticleProxyAdmin(ArticleAdminMixin):
    list_display = ('name', 'title', 'journal',)
    inlines = (ArticleDocumentInline,)

    def get_fields(self, request, *args, **kwargs):
        fields = super(ArticleProxyAdmin, self). get_fields(request, *args, **kwargs)

        exclude_fields = []
        if not request.user.is_superuser:
            exclude_fields.append('user')
            exclude_fields.append('journal')
            exclude_fields.append('editors')
            exclude_fields.append('assigned_editors')
            exclude_fields.append('reviewers')

        return [field for field in fields if field not in exclude_fields]

    def get_queryset(self, request):
        qs = super(ArticleProxyAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)

        return qs

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        else:
            return False

    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser :
            return self.readonly_fields
        else:
            readonly_fields = ['title', 'name', 'abstract']
            return readonly_fields


@admin.register(ArticleProxyT)
class ArticleProxyTAdmin(ArticleAdminMixin):
    list_display = ('name', 'title', 'journal',)
    inlines = (ArticleDocumentInline,)
    form = ArticleProxyTAdminForm

    def get_queryset(self, request):
        qs = super(ArticleProxyTAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(Q(journal__user=request.user)
                        | Q(journal__article__editors=request.user)
                        | Q(journal__article__assigned_editors=request.user)
                        | Q(journal__article__reviewers=request.user)
            )

        return qs

    def get_fields(self, request, *args, **kwargs):
        fields = super(ArticleProxyTAdmin, self).get_fields(request, *args, **kwargs)

        exclude_fields = []
        if not request.user.is_superuser:
            exclude_fields.append('user')
            exclude_fields.append('journal')

        return [field for field in fields if field not in exclude_fields]

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False

    def get_readonly_fields(self, request, obj=None):
        actions = super(ArticleProxyTAdmin, self). get_actions(request)

        if request.user.is_superuser:
            return self.readonly_fields
        else:
            readonly_fields = ['title', 'name', 'abstract']
            return readonly_fields
