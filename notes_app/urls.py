from django.urls import path
from .views import NoteListView, NoteCreateView, NoteDetailView

urlpatterns = [
    path('', NoteListView.as_view(), name='note-list'),
    path('create/', NoteCreateView.as_view(), name='note-create'),
    path('<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
]