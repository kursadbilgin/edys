# Django
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Local Django
from journal.models import Journal, Article, ArticleDocument

###     Journal     ###

class JournalAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def get_actions(self, request):
        actions = super(JournalAdmin, self).get_actions(request)

        if not request.user.is_superuser:
            del actions['delete_selected']

        return actions

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
        actions = super(JournalAdmin, self). get_actions(request)
        if request.user.is_superuser:
            return self.readonly_fields
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))

#############################


###     Article     ###

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')


#############################


###     Article Document     ###

class ArticleDocumentAdmin(admin.ModelAdmin):
    list_display = ('description', 'document')

#############################

admin.site.register(Journal, JournalAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleDocument, ArticleDocumentAdmin)
