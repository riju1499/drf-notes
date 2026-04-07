from django_filters import FilterSet, ChoiceFilter
from notes_app.models import Note

SHORT_NOTE_MAX_WORDS = 50

class NoteFilterSet(FilterSet):
    filter = ChoiceFilter(
        method='filter_by_length',
        choices=[
            ('short', f'Short Notes (< {SHORT_NOTE_MAX_WORDS} words)'),
            ('long', f'Long Notes (>= {SHORT_NOTE_MAX_WORDS} words)'),
        ],
        label='Filter by note length'
    )
    
    class Meta:
        model = Note
        fields = []
    
    def filter_by_length(self, queryset, name, value):
        
        if not value:
            return queryset
        
        value = value.lower().strip()
        
        if value == 'short':
            return queryset.filter(word_count__lt=SHORT_NOTE_MAX_WORDS)
        elif value == 'long':
            return queryset.filter(word_count__gte=SHORT_NOTE_MAX_WORDS)
        
        return queryset