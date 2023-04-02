from rest_framework import serializers
from web.models import User, Tag, Note
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class TagSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        self.validated_data['user_id'] = self.context['request'].user.id
        return super().save(**kwargs)

    class Meta:
        model = Tag
        fields = ('id', 'name')


class NoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True)

    def validate(self, attrs):
        if len(attrs['title']) > 15 or len(attrs['text']) > 100:
            raise ValidationError("Too many text")
        return attrs

    def save(self, **kwargs):
        tags = self.validated_data.pop('tag_ids')
        self.validated_data['user_id'] = self.context['request'].user.id
        self.validated_data['created_at'] = now()
        self.validated_data['updated_at'] = now()
        instance = super().save(**kwargs)
        instance.tags.set(tags)
        return instance

    class Meta:
        model = Note
        fields = ('id', 'title', 'text', 'user', 'tags', 'tag_ids')
