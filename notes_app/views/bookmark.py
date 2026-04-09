from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission

from notes_app.models import Note, Bookmark
from notes_app.serializers.bookmark import BookmarkSerializer
from notes_app.services.bookmark import create_bookmark, delete_bookmark
from notes_app.permissions import IsOwnerOrAdmin






class BookmarkListView(generics.ListAPIView):
    
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(
            user=self.request.user
        ).select_related('note', 'note__owner')


class BookmarkCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookmarkSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        note = data['note']
        if note.owner != request.user:
            return Response(
                {"error": "You can only bookmark notes that you own."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        bookmark = create_bookmark(request.user, note)

        response_serializer = BookmarkSerializer(bookmark, context={'request': request})
        return Response(
            {"message": "Note bookmarked successfully.", "bookmark": response_serializer.data},
            status=status.HTTP_201_CREATED
        )


class BookmarkDeleteView(APIView):
   
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def delete(self, request):
        note_id = request.data.get('note_id')
        if not note_id:
            return Response(
                {"error": "note_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            bookmark = Bookmark.objects.get(note_id=note_id)
        except Bookmark.DoesNotExist:
            return Response(
                {"error": "Bookmark not found for this note."},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, bookmark)

        delete_bookmark(bookmark)

        return Response(
            {"message": "Bookmark removed successfully."},
            status=status.HTTP_200_OK
        )