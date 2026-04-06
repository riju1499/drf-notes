from rest_framework import serializers
from notes_app.models import Note, Bookmark
from notes_app.serializers.note_serializers import NoteReadSerializer

class BookmarkSerializer(serializers.ModelSerializer):
    note_id = serializers.PrimaryKeyRelatedField(
        queryset=Note.objects.all(),
        source='note',
        write_only=True,
    )

    note_detail = NoteReadSerializer(source='note', read_only=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'note_id', 'note_detail', 'created_at']
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
