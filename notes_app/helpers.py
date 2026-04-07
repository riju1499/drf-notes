def extract_note_fields(data):
    return {
        "title": data.get("title"),
        "content": data.get("content"),
        "photo": data.get("photo"),
    }
