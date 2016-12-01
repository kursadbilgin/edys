# Django
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Local Django
from journal.models import Journal, Article, ArticleDocument

###     Journal     ###

class JournalAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


#############################


###     Article     ###

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')


#############################


###     Article Document     ###

class ArticleDocumentAdmin(admin.ModelAdmin):
    list_display = ('description',)


#############################

admin.site.register(Journal, JournalAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleDocument, ArticleDocumentAdmin)
