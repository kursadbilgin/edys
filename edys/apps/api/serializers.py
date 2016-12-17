# Third-Party
from rest_framework import serializers

# Local Django
from user.models import User
from core.models import Interest
from journal.models import Journal, Article, ArticleDocument


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class InterestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interest
        fields = ('name',)


class ArticleDocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleDocument
        fields = ('description', 'document')


class ArticleSerializer(serializers.ModelSerializer):
    article_documents = ArticleDocumentSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = ('name', 'article_documents')


class JournalSerializer(serializers.ModelSerializer):
    article = ArticleSerializer(read_only=True, many=True)

    class Meta:
        model = Journal
        fields = ('name', 'article')
