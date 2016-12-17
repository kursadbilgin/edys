# Django
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Local Django
from journal.models import Journal, Article, ArticleDocument
from core.variables import GROUP_EDITOR


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def get_actions(self, request):
        actions = super(JournalAdmin, self).get_actions(request)

        group_names = [group.name for group in request.user.groups.all()]
        if not request.user.is_superuser or GROUP_EDITOR in group_names:
            del actions['delete_selected']

        return actions

    def has_add_permission(self, request):
        group_names = [group.name for group in request.user.groups.all()]
        if request.user.is_superuser or GROUP_EDITOR in group_names:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        group_names = [group.name for group in request.user.groups.all()]
        if request.user.is_superuser or GROUP_EDITOR in group_names:
            return True
        else:
            return False

    def get_readonly_fields(self, request, obj=None):
        actions = super(JournalAdmin, self). get_actions(request)

        group_names = [group.name for group in request.user.groups.all()]
        if request.user.is_superuser or GROUP_EDITOR in group_names:
            return self.readonly_fields
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')


@admin.register(ArticleDocument)
class ArticleDocumentAdmin(admin.ModelAdmin):
    list_display = ('description', 'document')
