from notes_app.models import Note

def create_note(user, title, content, photo=None):
    title = title.strip().title()
    content = content.strip().capitalize()

    note = Note(
        owner=user,
        title=title,
        content=content,
        photo=photo,
    )

    note.full_clean() 
    note.save()

    return note

def update_note(note, *, title=None, content=None, photo=None):
    if title is not None:
        note.title = title.strip().title()

    if content is not None:
        note.content = content.strip().capitalize()

    if photo is not None:
        note.photo = photo

    note.full_clean()   
    note.save()

    return note