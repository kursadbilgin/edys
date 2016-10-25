# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.utils.translation import ugettext_lazy as _

# Local Django
from user.models import User
from user.forms import UserChangeForm

class UserAdmin(_UserAdmin):
    fieldsets = (
        (_(u'Base Informations'), {
            'fields' : ('email', 'password'),
        }),
        (_(u'Personal Informations'), {
            'fields' : ('first_name', 'last_name')
        }),
        (_(u'Important Informations'), {
            'fields' : ('last_login',)
        }),
        (_(u'Permissions'), {
            'fields' : ('is_active', 'is_staff', 'is_developer', 'is_superuser', 'user_permissions')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'affiliation', 'country', 'password1', 'password2',
                       'is_active', 'is_staff', 'is_developer')}
        ),
    )

    form = UserChangeForm

    list_display = ('first_name', 'last_name', 'email', 'is_active', 'is_staff',
                    'is_developer', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_developer')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login',)
    ordering = ('first_name', 'last_name')


admin.site.register(User, UserAdmin)
