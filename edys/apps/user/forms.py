# Django
from django import forms
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserChangeForm as _UserChangeForm


class CustomReadOnlyPasswordHashWidget(forms.Widget):
    def render(self, name, value, attrs):
        return format_html(_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"../password/\">this form</a>."
        ))


class CustomReadOnlyPasswordHashField(forms.Field):
    widget = CustomReadOnlyPasswordHashWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', False)
        super(CustomReadOnlyPasswordHashField, self).__init__(*args, **kwargs)

    def bound_data(self, data, initial):
        # Always return initial because the widget doesn't
        # render an input field.
        return initial

    def has_changed(self, initial, data):
        return False


class UserChangeForm(_UserChangeForm):
    password = CustomReadOnlyPasswordHashField(
        label=_('Password'),
    )
