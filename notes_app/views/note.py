from django.db.models import Q
from django.db.models.functions import Length
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from notes_app.helpers import extract_note_fields


from notes_app.models import Note
from notes_app.serializers.note import (
    NoteReadSerializer,
    NoteCreateSerializer,
    NoteUpdateSerializer,
)
from notes_app.services.note import create_note, update_note
from notes_app.filters import NoteFilterSet

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
        
        note = create_note(
    user=request.user,
    **extract_note_fields(serializer.validated_data)
)


        response_serializer = NoteReadSerializer(note, context={'request': request})
        return Response(
            {"message": "Note created successfully.", "note": response_serializer.data},
            status=status.HTTP_201_CREATED
        )


class NoteRetrieveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        note = Note.objects.filter(pk=pk, owner=request.user).first()
        if note is None:
            return Response({"error": "Note not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = NoteReadSerializer(note, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class NoteUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, pk):
        note = Note.objects.filter(pk=pk, owner=request.user).first()
        if note is None:
            return Response({"error": "Note not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = NoteUpdateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        note = update_note(note, serializer.validated_data)

        response_serializer = NoteReadSerializer(note, context={'request': request})
        return Response(
            {"message": "Note updated successfully.", "note": response_serializer.data},
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        note = Note.objects.filter(pk=pk, owner=request.user).first()
        if note is None:
            return Response({"error": "Note not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = NoteUpdateSerializer(
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        note = update_note(
    note,
    **extract_note_fields(serializer.validated_data)
)


        response_serializer = NoteReadSerializer(note, context={'request': request})
        return Response(
            {"message": "Note updated successfully.", "note": response_serializer.data},
            status=status.HTTP_200_OK
        )


class NoteDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        note = Note.objects.filter(pk=pk, owner=request.user).first()
        if note is None:
            return Response({"error": "Note not found."}, status=status.HTTP_404_NOT_FOUND)

        note_title = note.title
        note.delete()

        return Response(
            {"message": f"Note '{note_title}' deleted successfully."},
            status=status.HTTP_200_OK
        )