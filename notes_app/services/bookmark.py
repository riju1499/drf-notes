from notes_app.models import Bookmark

def create_bookmark(user, note):
    return Bookmark.objects.create(user=user, note=note)

def delete_bookmark(bookmark):
    bookmark.delete()