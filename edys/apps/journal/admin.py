# Django
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Local Django
from journal.models import Journal, Title, Article, ArticleDocument

###     Journal     ###

class JournalAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_titles')
    search_fields = ('name',)

#############################

###     Title     ###

class TitleAdmin(admin.ModelAdmin):
    list_display = ('name',)

#############################

###     Article     ###
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_titles')

#############################

###     Article Document     ###
class ArticleDocumentAdmin(admin.ModelAdmin):
    list_display = ('description',)

#############################

admin.site.register(Journal, JournalAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleDocument, ArticleDocumentAdmin)
