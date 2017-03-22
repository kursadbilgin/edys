# Django
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row

# Local Django
from user.models import User
from .forms import ArticleForm
from journal.models import Journal, Period, Article, ArticleDocument
from core.variables import GROUP_EDITOR
from core.variables import (
    USER_TYPES,
    USER_DEFAULT, USER_EDITOR,
    USER_ASSIGNEDEDITOR, USER_REVIEWER
)

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


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_users')
    search_fields = ('name',)

    def get_fields(self, request, *args, **kwargs):
        fields = super(JournalAdmin, self). get_fields(request, *args, **kwargs)

        exclude_fields = []
        if not request.user.is_superuser and not request.user.user_type==USER_EDITOR:
            exclude_fields.append('user')

        return [field for field in fields if field not in exclude_fields]

    def get_queryset(self, request):
        qs = super(JournalAdmin, self).get_queryset(request)

        if request.user.user_type==USER_EDITOR:
            qs = qs.filter(users=request.user.id)

        return qs

    def has_add_permission(self, request):
        if request.user.is_superuser or request.user.user_type==USER_EDITOR:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.user_type==USER_EDITOR:
            return True
        else:
            return False

    def get_actions(self, request):
        actions = super(JournalAdmin, self).get_actions(request)

        if not request.user.is_superuser and not request.user.user_type==USER_EDITOR:
            del actions['delete_selected']

        return actions

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser or not request.user.user_type==USER_EDITOR:
            obj.user = request.user

        obj.save()

    def get_readonly_fields(self, request, obj=None):
        actions = super(JournalAdmin, self). get_actions(request)

        if request.user.is_superuser or request.user.user_type==USER_EDITOR:
            return self.readonly_fields
        else:
            readonly_fields = ['users', 'name', 'content']
            return readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if not request.user.is_superuser and not request.user.user_type==USER_EDITOR:
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
        if not request.user.is_superuser or not request.user.user_type==USER_EDITOR:
            exclude_fields.append('user')

        return [field for field in fields if field not in exclude_fields]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "journal" and not request.user.is_superuser:
            kwargs["queryset"] = Journal.objects.filter(users=request.user)

        return super(PeriodAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(PeriodAdmin, self).get_queryset(request)

        if request.user.user_type==USER_EDITOR:
            qs = qs.filter(journal__period__user=request.user.id)

        return qs

    def has_add_permission(self, request):
        if request.user.is_superuser or request.user.user_type==USER_EDITOR:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or request.user.user_type==USER_EDITOR:
            return True
        else:
            return False

    def get_actions(self, request):
        actions = super(PeriodAdmin, self).get_actions(request)

        if not request.user.is_superuser and not request.user.user_type==USER_EDITOR:
            del actions['delete_selected']

        return actions

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser or not request.user.user_type==USER_EDITOR:
            obj.user = request.user

        obj.save()

    def get_readonly_fields(self, request, obj=None):
        actions = super(PeriodAdmin, self). get_actions(request)

        if request.user.is_superuser or request.user.user_type==USER_EDITOR:
            return self.readonly_fields
        else:
            readonly_fields = ['period', 'journal']
            return readonly_fields

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if not request.user.is_superuser and not request.user.user_type==USER_EDITOR:
            extra_context = extra_context or {}
            extra_context['show_save_and_add_another'] = False
            extra_context['show_save_and_continue'] = False
            extra_context['show_save'] = False
        return super(PeriodAdmin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'journal', 'period', 'user')
    inlines = (ArticleDocumentInline,)
    form = ArticleForm

    def get_fields(self, request, *args, **kwargs):
        fields = super(ArticleAdmin, self). get_fields(request, *args, **kwargs)

        exclude_fields = []
        if not request.user.is_superuser or not request.user.user_type==USER_EDITOR:
            exclude_fields.append('user')

        if not request.user.is_superuser:
            exclude_fields.append('period')

        if request.user.user_type==USER_DEFAULT or request.user.user_type==USER_REVIEWER:
            exclude_fields.append('assigned_editors') or exclude_fields.append('reviewers')

        if request.user.user_type==USER_ASSIGNEDEDITOR:
            exclude_fields.append('assigned_editors')

        return [field for field in fields if field not in exclude_fields]

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)

        return qs

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser or not request.user.user_type==USER_EDITOR:
            obj.user = request.user
        if not request.user.is_superuser:
            period = Period.objects.get()
            obj.period = period

        obj.save()


@admin.register(ArticleDocument)
class ArticleDocumentAdmin(admin.ModelAdmin):
    list_display = ('description', 'document')

    def get_queryset(self, request):
        qs = super(ArticleDocumentAdmin, self).get_queryset(request)

        if not request.user.is_superuser and not request.user.user_type==USER_EDITOR:
            qs = qs.filter(article__user=request.user.id)

        return qs
