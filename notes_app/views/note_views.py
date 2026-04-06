from django.db.models import Q
from django.db.models.functions import Length
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from notes_app.models import Note
from notes_app.serializers.note_serializers import (
    NoteReadSerializer,
    NoteCreateSerializer,
    NoteUpdateSerializer,
)
from notes_app.services.note import create_note, update_note
SHORT_NOTE_MAX_WORDS = 50


def get_filtered_notes(request):
    queryset = Note.objects.filter(owner=request.user)

    search = request.query_params.get('search', '').strip()
    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) | Q(content__icontains=search)
        )

    length_filter = request.query_params.get('filter', '').strip().lower()

    if length_filter == 'short':
        queryset = queryset.annotate(
            content_len=Length('content')
        ).filter(content_len__lt=SHORT_NOTE_MAX_WORDS * 6)

    elif length_filter == 'long':
        queryset = queryset.annotate(
            content_len=Length('content')
        ).filter(content_len__gte=SHORT_NOTE_MAX_WORDS * 6)

    sort = request.query_params.get('sort', 'newest').strip().lower()

    if sort == 'oldest':
        queryset = queryset.order_by('created_at')
    elif sort == 'updated':
        queryset = queryset.order_by('-updated_at')
    else:
        queryset = queryset.order_by('-created_at')

    return queryset


class NoteListView(generics.ListAPIView):
    serializer_class = NoteReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_filtered_notes(self.request)


class NoteCreateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = NoteCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        note = create_note(request.user, data = serializer.validated_data)

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

        note = update_note(note, serializer.validated_data)

        

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
