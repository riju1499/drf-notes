from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, Bookmark


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_bookmarked = serializers.SerializerMethodField()
    word_count = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = [
            'id',
            'owner',
            'title',
            'content',
            'word_count',
            'is_bookmarked',
            'created_at',
            'photo',
            'updated_at',
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


class BookmarkSerializer(serializers.ModelSerializer):
    note_id = serializers.PrimaryKeyRelatedField(
        queryset=Note.objects.all(),
        source='note',
        write_only=True,
    )

    note_detail = NoteSerializer(
        source='note',
        read_only=True,
    )

    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'note_id' ,'note_detail', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def validate(self, data):
        request = self.context.get('request')
        note = data.get('note')

        if note.owner != request.user:
            raise serializers.ValidationError(
                {"note_id": "You can only bookmark your own notes."}
            )

        if Bookmark.objects.filter(user=request.user, note=note).exists():
            raise serializers.ValidationError(
                {"note_id": "You have already bookmarked this note."}
            )

        return data