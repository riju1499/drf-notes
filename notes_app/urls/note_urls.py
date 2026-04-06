from django.urls import path
from notes_app.views.note_views import (
    NoteListView, NoteCreateView,
    NoteRetrieveView, NoteUpdateView, NoteDeleteView
)

urlpatterns = [
    path('', NoteListView.as_view(), name='note-list'),
    path('create/', NoteCreateView.as_view(), name='note-create'),
    path('<int:pk>/detail/', NoteRetrieveView.as_view(), name='note-detail'),
    path('<int:pk>/update/', NoteUpdateView.as_view(), name='note-update'),
    path('<int:pk>/delete/', NoteDeleteView.as_view(), name='note-delete'),
]
