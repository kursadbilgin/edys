# Django
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Local Django
from journal.models import Journal, Period, Article, ArticleDocument
from user.models import User
from core.variables import GROUP_EDITOR


class ArticleDocumentInline(admin.StackedInline):
    model = ArticleDocument
    extra = 0
    min_num = 1


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def get_actions(self, request):
        actions = super(JournalAdmin, self).get_actions(request)

        if not request.user.is_superuser or GROUP_EDITOR:
            del actions['delete_selected']

        return actions

    def has_add_permission(self, request):
        if request.user.is_superuser or GROUP_EDITOR:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or GROUP_EDITOR:
            return True
        else:
            return False

    def get_fields(self, request, *args, **kwargs):
        fields = super(JournalAdmin, self). get_fields(request, *args, **kwargs)

        exclude_fields = []
        if not request.user.is_superuser or not GROUP_EDITOR:
            exclude_fields.append('user')

        return [field for field in fields if field not in exclude_fields]

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser or not GROUP_EDITOR:
            obj.user = request.user

        obj.save()

    def get_readonly_fields(self, request, obj=None):
        actions = super(JournalAdmin, self). get_actions(request)

        if request.user.is_superuser or GROUP_EDITOR:
            return self.readonly_fields
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))

@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('period',)

    def get_actions(self, request):
        actions = super(PeriodAdmin, self).get_actions(request)

        if not request.user.is_superuser or GROUP_EDITOR:
            del actions['delete_selected']

        return actions

    def has_add_permission(self, request):
        if request.user.is_superuser or GROUP_EDITOR:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser or GROUP_EDITOR:
            return True
        else:
            return False

    def get_fields(self, request, *args, **kwargs):
        fields = super(PeriodAdmin, self). get_fields(request, *args, **kwargs)

        exclude_fields = []
        if not request.user.is_superuser or not GROUP_EDITOR:
            exclude_fields.append('user')

        return [field for field in fields if field not in exclude_fields]

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser or not GROUP_EDITOR:
            obj.user = request.user

        obj.save()


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = (ArticleDocumentInline,)
    list_display = ('name', 'title')

    def get_fields(self, request, *args, **kwargs):
        fields = super(ArticleAdmin, self). get_fields(request, *args, **kwargs)

        exclude_fields = []
        if not request.user.is_superuser or not GROUP_EDITOR:
            exclude_fields.append('user')

        return [field for field in fields if field not in exclude_fields]

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser or not GROUP_EDITOR:
            obj.user = request.user

        obj.save()

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)

        if not request.user.is_superuser or not GROUP_EDITOR:
            qs = qs.filter(pk=request.user.id)

        return qs


@admin.register(ArticleDocument)
class ArticleDocumentAdmin(admin.ModelAdmin):
    list_display = ('description', 'document')

    def get_queryset(self, request):
        qs = super(ArticleDocumentAdmin, self).get_queryset(request)

        if not request.user.is_superuser or not GROUP_EDITOR:
            qs = qs.filter(article__journal__user=request.user.id)

        return qs
