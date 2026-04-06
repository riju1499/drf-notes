from notes_app.models import Note

def create_note(user, data):
    return Note.objects.create(
        owner=user,
        title=data['title'],
        content=data['content'],
        photo=data.get('photo')
    )

def update_note(note, data):
    for field, value in data.items():
        setattr(note, field, value)
    note.save()
    return note