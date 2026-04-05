from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Note, Bookmark
from .serializers import BookmarkSerializer

class BookmarkListView(generics.ListAPIView):
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user).select_related('note', 'note__owner')

class BookmarkAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        note_id = request.data.get('note_id')
        if not note_id:
            return Response({"error": "note_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            note = Note.objects.get(pk=note_id)
        except Note.DoesNotExist:
            return Response({"error": "Note not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookmarkSerializer(data={'note_id': note_id}, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        bookmark = serializer.save(user=request.user)
        response_serializer = BookmarkSerializer(bookmark, context={'request': request})

        return Response({"message": "Note bookmarked successfully.", "bookmark": response_serializer.data},
                        status=status.HTTP_201_CREATED)

    def delete(self, request):
        note_id = request.data.get('note_id')
        if not note_id:
            return Response({"error": "note_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            bookmark = Bookmark.objects.get(user=request.user, note_id=note_id)
        except Bookmark.DoesNotExist:
            return Response({"error": "Bookmark not found for this note."}, status=status.HTTP_404_NOT_FOUND)

        bookmark.delete()
        return Response({"message": "Bookmark removed successfully."}, status=status.HTTP_200_OK)