from rest_framework import serializers
from web.models import User, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class NoteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    text = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    user = UserSerializer()
    tags = TagSerializer(many=True)