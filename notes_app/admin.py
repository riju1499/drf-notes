from django.contrib import admin
from .models import Note, Bookmark
 
 
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display  = ['id', 'owner', 'title', 'created_at', 'updated_at']
    list_filter   = ['owner', 'created_at']
    search_fields = ['title', 'content', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']
 
 
@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display  = ['id', 'user', 'note', 'created_at']
    list_filter   = ['user']
    readonly_fields = ['created_at']
 
