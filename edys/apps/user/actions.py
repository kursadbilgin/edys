# Django
from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.models import Permission, Group
from django.utils.translation import ugettext_lazy as _

#
# def make_editor(modeladmin, request, queryset):
#     for user in queryset:
#         try:
#             group = Group.objects.get(name='Editor')
#             user.groups.clear()
#             user.groups.add(group)
#             user.user_type = USER_EDITOR
#             user.save_base()
#             messages.success(request, _("Seçilen kullanıcı editör yapıldı."))
#         except Group.DoesNotExist:
#             messages.error(request, _("Böyle bir grup bulunamadı"))
# make_editor.short_description = _("Make selected editor")
#
