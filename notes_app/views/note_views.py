from django.db.models.functions import Length
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from notes_app.models import Note
from notes_app.serializers.note_serializers import (
    NoteReadSerializer, NoteCreateSerializer, NoteUpdateSerializer
)

SHORT_NOTE_MAX_WORDS = 50

def get_filtered_notes(request):
    queryset = Note.objects.filter(owner=request.user)

    search = request.query_params.get('search', '').strip()
    if search:
        queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))

    length_filter = request.query_params.get('filter', '').strip().lower()
    if length_filter == 'short':
        queryset = queryset.annotate(content_len=Length('content')).filter(
            content_len__lt=SHORT_NOTE_MAX_WORDS * 6
        )
    elif length_filter == 'long':
        queryset = queryset.annotate(content_len=Length('content')).filter(
            content_len__gte=SHORT_NOTE_MAX_WORDS * 6
        )

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


class NoteCreateView(generics.GenericAPIView):
    serializer_class = NoteCreateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        note = Note.objects.create(
            owner=request.user,
            title=data['title'],
            content=data['content'],
            photo=data.get('photo')
        )

        return Response(
            {"message": "Note created successfully.",
             "note": NoteReadSerializer(note, context={'request': request}).data},
            status=status.HTTP_201_CREATED
        )


class NoteRetrieveView(generics.RetrieveAPIView):
    serializer_class = NoteReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)


class NoteUpdateView(generics.GenericAPIView):
    serializer_class = NoteUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request, pk):
        note = Note.objects.get(pk=pk, owner=request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        for field, value in data.items():
            setattr(note, field, value)
        note.save()

        return Response(
            {"message": "Note updated successfully.",
             "note": NoteReadSerializer(note, context={'request': request}).data},
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        note = Note.objects.get(pk=pk, owner=request.user)
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        for field, value in data.items():
            setattr(note, field, value)
        note.save()

        return Response(
            {"message": "Note updated successfully.",
             "note": NoteReadSerializer(note, context={'request': request}).data},
            status=status.HTTP_200_OK
        )


class NoteDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user)
