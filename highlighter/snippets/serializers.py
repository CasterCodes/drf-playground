from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


"""
  Example of a raw serializer
"""

# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=True,allow_blank=True,max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=True)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

#     def create(self, validated_data):
#         """
#         Create and return new instance of `Snippet` instance given data
#         """

#         return Snippet.objects.create(validated_data)
#     def update(self, instance, validated_data):
#         """
#         Update and return new instance of `Snippet` instance given data
#         """

#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)

#         instance.save()

#         return instance

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name="snippet-highlight", format='html')
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'highlight', 'linenos', 'language', 'style', 'owner']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-list', read_only=True)

    class Meta:
        model = User
        fields = ['id','username', 'snippets']