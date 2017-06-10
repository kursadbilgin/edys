# Third-Party
from redactor.widgets import RedactorEditor

# Django
from django import forms
from django.conf import settings
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType

# Local Django
from journal.models import Journal, Article
from journal.extension import UPLOAD_DOCUMENT_TYPE


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
           'abstract': RedactorEditor(),
        }


class ArticleDocumentAdminForm(forms.ModelForm):
    document = forms.FileField(label=_('Document'))

    def clean_document(self):
         document = self.cleaned_data['document']

         if 'document' in self.changed_data:

             if not document.content_type in UPLOAD_DOCUMENT_TYPE:
                 raise forms.ValidationError(
                    _('Please only upload document (doc, pdf, txt, exel, powerpoint).')
                )

         return document


class ArticleProxyTAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ArticleProxyTAdminForm, self).__init__(*args, **kwargs)
        self.fields['editors'].queryset = self.instance.journal.editors.all()
        self.fields['assigned_editors'].queryset = self.instance.journal.assigned_editors.all()
