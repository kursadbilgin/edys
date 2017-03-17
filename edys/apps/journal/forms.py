#Django
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

#Local Django
from journal.models import *

class CustomModelChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         journal = Journal.objects.get()
         period = Period.objects.get()
         return "%s, %s" % (journal, period)


class ArticleForm(forms.ModelForm):
    journal = CustomModelChoiceField(queryset=Journal.objects.all(), label=_("Journal"))

    class Meta:
        fields = "__all__"
        model = Article
