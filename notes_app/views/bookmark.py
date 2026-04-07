from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from notes_app.models import Note, Bookmark
from notes_app.serializers.bookmark import BookmarkSerializer
from notes_app.services.bookmark import create_bookmark, delete_bookmark



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
        bookmark = create_bookmark(request.user, data['note'])


        response_serializer = BookmarkSerializer(bookmark, context={'request': request})
        return Response(
            {"message": "Note bookmarked successfully.", "bookmark": response_serializer.data},
            status=status.HTTP_201_CREATED
        )


class BookmarkDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        note_id = request.data.get('note_id')
        if not note_id:
            return Response({"error": "note_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        bookmark = Bookmark.objects.filter(user=request.user, note_id=note_id).first()
        if not bookmark:
            return Response({"error": "Bookmark not found for this note."},
                            status=status.HTTP_404_NOT_FOUND)

        delete_bookmark(bookmark)

        return Response({"message": "Bookmark removed successfully."},
                        status=status.HTTP_200_OK)
