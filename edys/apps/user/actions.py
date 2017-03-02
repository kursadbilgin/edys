# Django
from django.contrib import admin
from django.contrib.auth.models import Permission, Group
from django.utils.translation import ugettext_lazy as _

# Local Django
from core.variables import (
    USER_TYPES,
    USER_DEFAULT, USER_EDITOR,
    USER_ASSIGNEDEDITOR, USER_REVIEWER
)

def make_editor(modeladmin, request, queryset):
    queryset.update(user_type=USER_EDITOR)
make_editor.short_description = _("Make selected editor")

def make_assignededitor(modeladmin, request, queryset):
    queryset.update(user_type=USER_ASSIGNEDEDITOR)
make_assignededitor.short_description = _("Make selected assigned editor")

def make_reviewer(modeladmin, request, queryset):
    queryset.update(user_type=USER_REVIEWER)
make_reviewer.short_description = _("Make selected reviewer")

def make_default(modeladmin, request, queryset):
    queryset.update(user_type=USER_DEFAULT)
make_default.short_description = _("Make selected user")
