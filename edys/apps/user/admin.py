# Standard Library
from copy import deepcopy

# Django
from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

# Local Django
from user.mixins import UserAdminMixin
from user.models import (
    UserDefault, UserEditor, UserAssignedEditor, UserReviewer
)
from core.variables import (
    GROUP_DEFAULT, GROUP_EDITOR, GROUP_ASSIGNEDEDITOR, GROUP_REVIEWER
)


@admin.register(UserDefault)
class UserDefaultAdmin(UserAdminMixin):
    def save_model(self, request, obj, form, change):
        obj.save()

        try:
            group = Group.objects.get(name=GROUP_DEFAULT)
            group.user_set.add(obj)
        except Group.DoesNotExist:
            pass



@admin.register(UserEditor)
class UserEditorAdmin(UserAdminMixin):
    def save_model(self, request, obj, form, change):
        obj.is_editor = True
        obj.save()

        try:
            group = Group.objects.get(name=GROUP_EDITOR)
            group.user_set.add(obj)
        except Group.DoesNotExist:
            pass



@admin.register(UserAssignedEditor)
class UserAssignedEditorAdmin(UserAdminMixin):
    def save_model(self, request, obj, form, change):
        obj.is_assigned_editor = True
        obj.save()

        try:
            group = Group.objects.get(name=GROUP_ASSIGNEDEDITOR)
            group.user_set.add(obj)
        except Group.DoesNotExist:
            pass


@admin.register(UserReviewer)
class UserReviewerAdmin(UserAdminMixin):
    def save_model(self, request, obj, form, change):
        obj.is_reviewer = True
        obj.save()

        try:
            group = Group.objects.get(name=GROUP_REVIEWER)
            group.user_set.add(obj)
        except Group.DoesNotExist:
            pass
