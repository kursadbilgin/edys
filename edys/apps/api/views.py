# Third-Party
from rest_framework import viewsets

# Local Django
from user.models import User

# Api
from api.serializers import UserSerializer

###     User     ###

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

########################


LIST = (
     (r'user', UserViewSet),
 )
