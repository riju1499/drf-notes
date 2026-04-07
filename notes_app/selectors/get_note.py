from notes_app.models import Note
from rest_framework.exceptions import NotFound

def get_note_by_id(note_id, user):
    note=Note.objects.filter(pk=note_id, owner=user).first()
    if not note:
        raise NotFound("Note not found")
    return note

