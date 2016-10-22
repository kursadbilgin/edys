# Standard Library
import getpass

# Local Django
from edys.settings.base import *


if getpass.getuser() in ['root']:
    from edys.settings.production import *
else:
    from edys.settings.dev import *
