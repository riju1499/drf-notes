from notes_app.models import Note

def create_note(user, title, content, photo=None):
    title = title.strip().title() 
    content = content.strip().capitalize() 
    return Note.objects.create(
        owner=user,
        title=title,
        content=content,
        photo=photo,
    )

def update_note(note, *, title=None, content=None, photo=None):
    if title is not None:
        note.title = title
    if content is not None:
        note.content = content
    if photo is not None:
        note.photo = photo

    note.save()
    return note
