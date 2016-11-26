# Third-Party
from rest_framework import serializers

# Local Django
from user.models import User
from core.models import Interest
from journal.models import Journal, Title, Article, ArticleDocument

###     User     ###

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

####################

###     Interest     ###

class InterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interest
        fields = ('name',)

####################

###     Article Document     ###

class ArticleDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleDocument
        fields = ('description', 'document')

####################

###     Article     ###

class ArticleSerializer(serializers.ModelSerializer):
    article_documents = ArticleDocumentSerializer(read_only=True, many=True)


    class Meta:
        model = Article
        fields = ('name', 'article_documents')

####################

###     Title     ###

class TitleSerializer(serializers.ModelSerializer):
    article_set = ArticleSerializer(read_only=True, many=True)

    class Meta:
        model = Title
        fields = ('name', 'article_set')

####################

###     Journal     ###

class JournalSerializer(serializers.ModelSerializer):
    titles = TitleSerializer(read_only=True, many=True)

    class Meta:
        model = Journal
        fields = ('name', 'titles')

####################
