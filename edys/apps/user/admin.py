# Standard Library
from copy import deepcopy

# Django
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.utils.translation import ugettext_lazy as _

# Local Django
from user.models import User
from user.forms import UserChangeForm
from core.variables import GROUP_DEFAULT, GROUP_EDITOR

class UserAdmin(_UserAdmin):
    fieldsets = (
        (_(u'Base Informations'), {
            'fields' : ('email', 'password'),
        }),
        (_(u'Personal Informations'), {
            'fields' : ('first_name', 'last_name'),
        }),
        (_(u'Important Informations'), {
            'fields' : ('last_login',),
        }),
        (_(u'Permissions'), {
            'fields' : ('is_active', 'is_staff', 'is_developer', 'groups', 'is_superuser', 'user_permissions'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'affiliation', 'country', 'password1', 'password2',
                       'is_active', 'is_staff', 'is_developer', 'is_superuser', 'groups')}
        ),
    )

    form = UserChangeForm

    list_display = ('first_name', 'last_name', 'email', 'is_active', 'is_staff',
                    'is_developer', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_developer')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login',)
    ordering = ('first_name', 'last_name')


    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.exclude(is_superuser=True)

            group_names = [group.name for group in request.user.groups.all()]
            if not GROUP_EDITOR in group_names:
                qs = qs.filter(pk=request.user.id)

        return qs

    def save_model(self, request, obj, form, change):
        obj.save()

        try:
            group = Group.objects.get(name=GROUP_DEFAULT)
            group.user_set.add(obj)
        except Group.DoesNotExist:
            pass

    def delete_selected(self, request, obj):
        for user in obj.all():
            if not user.is_superuser:
                user.delete()

    delete_selected.short_description = _("Delete selected Users")

    def get_actions(self, request):
        group_names = [group.name for group in request.user.groups.all()]
        actions = super(UserAdmin, self).get_actions(request)

        if not request.user.is_superuser and not GROUP_EDITOR in group_names:
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

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(UserAdmin, self).get_fieldsets(request, obj)

        group_names = [group.name for group in request.user.groups.all()]

        custom_fieldsets = deepcopy(fieldsets)

        if not request.user.is_superuser and not GROUP_EDITOR in group_names:

            if obj == request.user:
                custom_fieldsets = [field for field in custom_fieldsets if field[0] != _('Permissions')]

            for fieldset in custom_fieldsets:
                fields = [field for field in fieldset[1]['fields'] if field not in ['is_superuser', 'is_developer']]
                fieldset[1]['fields'] = fields

        return custom_fieldsets


admin.site.register(User, UserAdmin)
