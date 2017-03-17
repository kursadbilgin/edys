# Django
from django.utils.translation import ugettext_lazy as _


# USER
USER_DEFAULT, USER_EDITOR, USER_ASSIGNEDEDITOR, USER_REVIEWER = (0, 1, 2, 3)
USER_TYPES = (
    (USER_DEFAULT, _('Default')),
    (USER_EDITOR, ('Editor')),
    (USER_ASSIGNEDEDITOR, _('Assigned Editor')),
    (USER_REVIEWER, _('Reviewer'))
)

# Group
GROUP_DEFAULT = _('Default')
GROUP_EDITOR = ('Editor')
GROUP_ASSIGNEDEDITOR = _('Assigned Editor')
GROUP_REVIEWER = _('Reviewer')
