# Third-Party
from rest_framework import viewsets

# Local Django
from user.models import User
from core.models import Interest
from journal.models import Journal, Article, ArticleDocument

# Api
from api.serializers import UserSerializer, JournalSerializer

###     User     ###

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

########################


###     Journal     ###

class JournalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Journal.objects.all()
    serializer_class = JournalSerializer

####################

LIST = (
     (r'user', UserViewSet),
     (r'journal', JournalViewSet)
 )
