from django.urls import path
from .bookmark_views import BookmarkListView, BookmarkAPIView
 
urlpatterns = [
    # GET-only list of bookmarked notes (ListAPIView)
    path('', BookmarkListView.as_view(), name='bookmark-list'),
 
    # POST (add) + DELETE (remove) a bookmark (APIView)
    path('manage/', BookmarkAPIView.as_view(), name='bookmark-manage'),
]
 