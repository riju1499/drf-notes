from rest_framework import serializers
from notes_app.models import Note, Bookmark

class NoteReadSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_bookmarked = serializers.SerializerMethodField()
    word_count = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            'id', 'owner', 'title', 'content', 'word_count',
            'is_bookmarked', 'created_at', 'photo', 'updated_at'
        ]
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Bookmark.objects.filter(user=request.user, note=obj).exists()
        return False

    def get_word_count(self, obj):
        return len(obj.content.split())

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be blank or just spaces.")
        return value.strip()

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be blank or just spaces.")
        return value.strip()


class NoteCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    content = serializers.CharField()
    photo = serializers.ImageField(required=False)

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be blank or just spaces.")
        return value.strip()

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be blank or just spaces.")
        return value.strip()


class NoteUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)
    photo = serializers.ImageField(required=False)

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be blank or just spaces.")
        return value.strip()

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be blank or just spaces.")
        return value.strip()
