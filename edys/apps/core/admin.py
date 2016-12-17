# Django
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

# Local Django
from core.models import Interest


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def get_fields(self, request, *args, **kwargs):
        fields = super(InterestAdmin, self).get_fields(request, *args, **kwargs)

        exclude_fields = []
        if 'add' in request.path.split('/'):
            exclude_fields = ['create_date', 'update_date']

        return [field for field in fields if field not in exclude_fields]
