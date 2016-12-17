# Django
from django.db.models import Q
from django.contrib.auth.models import Permission, Group

# Local Django
from core.variables import (
    GROUP_DEFAULT, GROUP_REVIEWER,
    GROUP_EDITOR, GROUP_ASSIGNEDEDITOR
)


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

    create_group(GROUP_DEFAULT, user_permissions)

def editor():
    user_permissions = [
        p for p in Permission.objects.filter(
            Q(content_type__app_label__in=['user'])
            & Q(codename__icontains='user')
        )
    ]

    journal_permissions = [
        p for p in Permission.objects.filter(
            Q(content_type__app_label__in=['journal'])
        )
    ]

    create_group(GROUP_EDITOR, (user_permissions + journal_permissions))


def assigned_editor():
    user_permissions = [
        p for p in Permission.objects.filter(
            Q(content_type__app_label__in=['user'])
            & Q(codename__icontains='user')
        )
    ]

    journal_permissions = [
        p for p in Permission.objects.filter(
            Q(content_type__app_label__in=['journal'])
        )
    ]

    create_group(GROUP_ASSIGNEDEDITOR, (user_permissions + journal_permissions))


def reviewer():
    user_permissions = [
        p for p in Permission.objects.filter(
            Q(content_type__app_label__in=['user'])
            & Q(codename__icontains='user')
        )
    ]

    journal_permissions = [
        p for p in Permission.objects.filter(
            Q(content_type__app_label__in=['journal'])
        )
    ]

    create_group(GROUP_REVIEWER, (user_permissions + journal_permissions))
