# Django
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class JournalConfig(AppConfig):
    name = 'journal'
    verbose_name = _('Journal')
