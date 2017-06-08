# Django
from django.db.models import Q
from django.contrib.auth.models import Permission, Group

# Local Django
from core.variables import GROUP_DEFAULT, GROUP_ADMIN


def create_group(group_name, permissions):
    try:
        group = Group.objects.get(name=group_name)

        group.permissions.clear()
        group.permissions.add(*permissions)
    except Group.DoesNotExist:
        group = Group.objects.create(name=group_name)
        group.permissions.add(*permissions)


def default():
    user_permissions = [
        p for p in Permission.objects.filter(
            Q(content_type__app_label__in=['user'])
            & Q(codename__icontains='user')
        )
    ]

    journal_permissions = [
        p for p in Permission.objects.filter(
            Q(content_type__app_label__in=['journal'])
            & Q(codename__icontains='journal')
            | Q(codename__icontains='period')
            | Q(codename__icontains='article')
            | Q(codename__icontains='articleproxy')
        )
    ]

    create_group(GROUP_DEFAULT, (user_permissions + journal_permissions))

def admin():
    user_permissions = [
        p for p in Permission.objects.filter(
            Q(content_type__app_label__in=['user'])
        )
    ]

    journal_permissions = [
        p for p in Permission.objects.filter(
            Q(content_type__app_label__in=['journal'])
            & Q(codename__icontains='journal')
            | Q(codename__icontains='period')
            | Q(codename__icontains='article')
            | Q(codename__icontains='articleproxy')
        )
    ]

    create_group(GROUP_ADMIN, (user_permissions + journal_permissions))
