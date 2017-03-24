#Django
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

#Local Django
from journal.models import *
from core.variables import (USER_TYPES, USER_EDITOR)

class CustomModelChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         try:
             period = Period.objects.get(id=obj.id)
             journals = period.journal
             return "%s, %s" % (period, journals)
         except:
             return super(CustomModelChoiceField, self).label_from_instance(obj)

class ModelMultipleChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         try:
             editor = UserEditor.objects.get(id=obj.id)
             journals = editor.journal_set.all()
             journals_name = ', '.join([journal.name for journal in journals])
             return "%s - %s" % (editor, journals_name)
         except:
             return super(ModelMultipleChoiceField, self).label_from_instance(obj)

class ArticleForm(forms.ModelForm):
    period = CustomModelChoiceField(
        queryset=Period.objects.all(), label=_("Period")
    )
    editors = ModelMultipleChoiceField(
        queryset=User.objects.filter(user_type=USER_EDITOR), label=_("Editors"),
        widget=forms.SelectMultiple
    )

    class Meta:
        fields = "__all__"
        model = Article
