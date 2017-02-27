# Standard Library
from copy import deepcopy

# Django
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

# Local Django
from user.models import Interest
from user.actions import *
from user.mixins import UserAdminMixin
from user.models import (
    UserDefault, UserEditor, UserAssignedEditor, UserReviewer
)
from core.variables import (
    GROUP_DEFAULT, GROUP_EDITOR, GROUP_ASSIGNEDEDITOR, GROUP_REVIEWER
)


@admin.register(UserDefault)
class UserDefaultAdmin(UserAdminMixin):
    actions = [make_editor, make_assignededitor, make_reviewer]

    def save_model(self, request, obj, form, change):
        obj.save()

        try:
            group = Group.objects.get(name=GROUP_DEFAULT)
            group.user_set.add(obj)
        except Group.DoesNotExist:
            pass



@admin.register(UserEditor)
class UserEditorAdmin(UserAdminMixin):
    actions = [make_assignededitor, make_reviewer, make_default]

    def save_model(self, request, obj, form, change):
        obj.save()

        try:
            group = Group.objects.get(name=GROUP_EDITOR)
            group.user_set.add(obj)
        except Group.DoesNotExist:
            pass



@admin.register(UserAssignedEditor)
class UserAssignedEditorAdmin(UserAdminMixin):
    actions = [make_editor, make_reviewer, make_default]

    def save_model(self, request, obj, form, change):
        obj.save()

        try:
            group = Group.objects.get(name=GROUP_ASSIGNEDEDITOR)
            group.user_set.add(obj)
        except Group.DoesNotExist:
            pass


@admin.register(UserReviewer)
class UserReviewerAdmin(UserAdminMixin):
    actions = [make_editor, make_assignededitor, make_default]


    def save_model(self, request, obj, form, change):
        obj.save()

        try:
            group = Group.objects.get(name=GROUP_REVIEWER)
            group.user_set.add(obj)
        except Group.DoesNotExist:
            pass


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user')

    def get_fields(self, request, *args, **kwargs):
        fields = super(InterestAdmin, self).get_fields(request, *args, **kwargs)

        exclude_fields = []
        if 'add' in request.path.split('/'):
            exclude_fields = ['create_date', 'update_date']

        return [field for field in fields if field not in exclude_fields]
