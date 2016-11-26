# Third-Party
from rest_framework import serializers

# Local Django
from user.models import User

###     User     ###

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

####################
