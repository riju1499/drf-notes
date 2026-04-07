from django.db.models import Q
from django.db.models.functions import Length
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


from notes_app.models import Note
from notes_app.serializers.note import (
    NoteReadSerializer,
    NoteCreateSerializer,
    NoteUpdateSerializer,
)
from notes_app.services.note import create_note, update_note
from notes_app.filters import NoteFilterSet
from notes_app.selectors.get_note import get_note_by_id


SHORT_NOTE_MAX_WORDS = 50


class NoteListView(generics.ListAPIView):
    serializer_class = NoteReadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = NoteFilterSet
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


class NoteCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = NoteCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        note = create_note(
            user=request.user,
            title=data["title"],
            content=data["content"],
            photo=data.get("photo"),
)


        response_serializer = NoteReadSerializer(note, context={'request': request})
        return Response(
            {"message": "Note created successfully.", "note": response_serializer.data},
            status=status.HTTP_201_CREATED
        )


class NoteRetrieveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        note = get_note_by_id(pk, request.user)

        
        serializer = NoteReadSerializer(note, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class NoteUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def update(self, request, pk, partial=False):
        
        note = get_note_by_id(pk, request.user)

        serializer = NoteUpdateSerializer(
            data=request.data,
            partial=partial,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

       
        note = update_note(note, **serializer.validated_data)

        response_serializer = NoteReadSerializer(note, context={'request': request})
        return Response(
            {"message": "Note updated successfully.", "note": response_serializer.data},
            status=status.HTTP_200_OK
        )

    def put(self, request, pk):
        
        return self.update(request, pk, partial=False)

    def patch(self, request, pk):
       
        return self.update(request, pk, partial=True)

class NoteDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        note = get_note_by_id(pk, request.user)

    

        note_title = note.title
        note.delete()

        return Response(
            {"message": f"Note '{note_title}' deleted successfully."},
            status=status.HTTP_200_OK
        )