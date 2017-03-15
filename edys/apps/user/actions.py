# Django
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.models import Permission, Group
from django.utils.translation import ugettext_lazy as _

# Local Django
from core.variables import (
    USER_TYPES,
    USER_DEFAULT, USER_EDITOR,
    USER_ASSIGNEDEDITOR, USER_REVIEWER
)

def make_editor(modeladmin, request, queryset):
    for user in queryset:
        try:
            group = Group.objects.get(name='Editor')
            user.groups.clear()
            user.groups.add(group)
            user.user_type = USER_EDITOR
            user.save_base()
            messages.success(request, _("Seçilen kullanıcı editör yapıldı."))
        except Group.DoesNotExist:
            messages.error(request, _("Böyle bir grup bulunamadı"))
make_editor.short_description = _("Make selected editor")

def make_assignededitor(modeladmin, request, queryset):
    for user in queryset:
        try:
            group = Group.objects.get(name='Assigned Editor')
            user.groups.clear()
            user.groups.add(group)
            user.user_type = USER_ASSIGNEDEDITOR
            user.save_base()
            messages.success(request, _("Seçilen kullanıcı atanan editör yapıldı."))
        except Group.DoesNotExist:
            messages.error(request, _("Böyle bir grup bulunamadı"))
make_assignededitor.short_description = _("Make selected assigned editor")

def make_reviewer(modeladmin, request, queryset):
    for user in queryset:
        try:
            group = Group.objects.get(name='Reviewer')
            user.groups.clear()
            user.groups.add(group)
            user.user_type = USER_REVIEWER
            user.save_base()
            messages.success(request, _("Seçilen kullanıcı denetleyici yapıldı."))
        except Group.DoesNotExist:
            messages.error(request, _("Böyle bir grup bulunamadı"))
make_reviewer.short_description = _("Make selected reviewer")

def make_default(modeladmin, request, queryset):
    for user in queryset:
        try:
            group = Group.objects.get(name='Default')
            user.groups.clear()
            user.groups.add(group)
            user.user_type = USER_DEFAULT
            user.save_base()
            messages.success(request, _("Seçilen kullanıcı normal kullanıcı yapıldı."))
        except Group.DoesNotExist:
            messages.error(request, _("Böyle bir grup bulunamadı"))
make_default.short_description = _("Make selected user")
