# Standard Library
from copy import deepcopy

# Django
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as _UserAdmin

# Local Django
from user.forms import UserChangeForm
from user.models import User, Interest
from core.variables import GROUP_DEFAULT, GROUP_EDITOR


class InterestInline(admin.StackedInline):
    model = Interest
    extra = 0


class UserAdminMixin(_UserAdmin):
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
            'fields' : ('is_active',),
        }),
        (_(u'Secret Permissions'), {
            'fields' : ('is_staff', 'is_superuser'),
        }),
        (_(u'Groups'), {
            'fields' : ('groups', 'user_permissions'),
        })
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'affiliation',
                       'country', 'password1', 'password2')}
        ),
    )

    form = UserChangeForm

    list_display = ('first_name', 'last_name', 'email', 'is_active',
                    'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login',)
    ordering = ('first_name', 'last_name')
    inlines = (InterestInline,)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(UserAdminMixin, self).get_fieldsets(request, obj)

        custom_fieldsets = deepcopy(fieldsets)
        group_names = [group.name for group in request.user.groups.all()]

        if not request.user.is_superuser and not GROUP_EDITOR in group_names:
            exclude_fieldsets = [ _('Permissions'), _('Secret Permissions'),
                                 _('Groups')]

            custom_fieldsets = [
                field for field in custom_fieldsets if field[0] not in exclude_fieldsets
            ]

        return custom_fieldsets

    def get_queryset(self, request):
        qs = super(UserAdminMixin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.exclude(is_superuser=True)

            group_names = [group.name for group in request.user.groups.all()]
            if not GROUP_EDITOR in group_names:
                qs = qs.filter(pk=request.user.id)

        return qs

    def delete_selected(self, request, obj):
        group_names = [group.name for group in request.user.groups.all()]
        for user in obj.all():
            if not user.is_superuser or not GROUP_EDITOR in group_names:
                user.delete()

    delete_selected.short_description = _("Delete selected Users")

    def get_actions(self, request, obj=None):
        actions = super(UserAdminMixin, self).get_actions(request)
        group_names = [group.name for group in request.user.groups.all()]

        if not request.user.is_superuser and not GROUP_EDITOR in group_names:
            actions = []

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
