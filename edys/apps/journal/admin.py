# Django
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Local Django
from user.models import User
from journal.models import Journal, Period, Article, ArticleDocument
from core.variables import GROUP_EDITOR
from core.variables import (
    USER_TYPES,
    USER_DEFAULT, USER_EDITOR,
    USER_ASSIGNEDEDITOR, USER_REVIEWER
)


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

        if not request.user.is_superuser:
            qs = qs.filter(users=request.user)

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

    def get_readonly_fields(self, request, obj=None):
        actions = super(JournalAdmin, self). get_actions(request)

        if request.user.is_superuser or request.user.user_type==USER_EDITOR:
            return self.readonly_fields
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser or not request.user.user_type==USER_EDITOR:
            obj.user = request.user

        obj.save()


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

    def get_queryset(self, request):
        qs = super(PeriodAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)

        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "journal" and not request.user.is_superuser:
            kwargs["queryset"] = Journal.objects.filter(users=request.user)

        return super(PeriodAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

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

    def get_readonly_fields(self, request, obj=None):
        actions = super(PeriodAdmin, self). get_actions(request)

        if request.user.is_superuser or request.user.user_type==USER_EDITOR:
            return self.readonly_fields
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser or not request.user.user_type==USER_EDITOR:
            obj.user = request.user

        obj.save()


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'journal', 'period', 'user')
    inlines = (ArticleDocumentInline,)

    def get_fields(self, request, *args, **kwargs):
        fields = super(ArticleAdmin, self). get_fields(request, *args, **kwargs)

        exclude_fields = []
        if not request.user.is_superuser or not request.user.user_type==USER_EDITOR:
            exclude_fields.append('user')

        return [field for field in fields if field not in exclude_fields]

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)

        return qs

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser or not request.user.user_type==USER_EDITOR:
            obj.user = request.user

        obj.save()


@admin.register(ArticleDocument)
class ArticleDocumentAdmin(admin.ModelAdmin):
    list_display = ('description', 'document')

    def get_queryset(self, request):
        qs = super(ArticleDocumentAdmin, self).get_queryset(request)

        if not request.user.is_superuser and not request.user.user_type==USER_EDITOR:
            qs = qs.filter(article__journal__users=request.user.id)

        return qs
