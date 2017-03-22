#Django
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

#Local Django
from journal.models import *
# from core.variables import GROUP_EDITOR
from core.variables import (USER_TYPES, USER_EDITOR)

class CustomModelChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         journal = Journal.objects.get()
         period = Period.objects.get()
         return "%s, %s" % (journal, period)

class ModelMultipleChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         user = User.objects.get(user_type=USER_EDITOR)
         journal = Journal.objects.get()
         return "%s, %s" % (user, journal)


class ArticleForm(forms.ModelForm):
    journal = CustomModelChoiceField(
        queryset=Journal.objects.all(), label=_("Journal")
    )
    editors = ModelMultipleChoiceField(
        queryset=User.objects.filter(user_type=USER_EDITOR), label=_("Editors"),
        widget=forms.SelectMultiple
    )

    class Meta:
        fields = "__all__"
        model = Article
