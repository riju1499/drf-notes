from django.urls import path
from notes_app.views.bookmark_views import (
    BookmarkListView, BookmarkCreateView, BookmarkDeleteView
)

urlpatterns = [
    path('', BookmarkListView.as_view(), name='bookmark-list'),
    path('create/', BookmarkCreateView.as_view(), name='bookmark-create'),
    path('delete/', BookmarkDeleteView.as_view(), name='bookmark-delete'),
]
