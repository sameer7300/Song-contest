from django import forms
from .models import Song, Vote, Comment, Category, Tag

class SongUploadForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'description', 'language', 'genre', 'tags', 'ai_tool_used', 'audio_file', 'lyrics_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter song title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your song...'}),
            'language': forms.Select(attrs={'class': 'form-select'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.CheckboxSelectMultiple(),
            'ai_tool_used': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Suno AI, Boomy, etc.'}),
            'audio_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.mp3,.wav'}),
            'lyrics_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.txt,.pdf,.doc,.docx'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if hasattr(field.widget, 'attrs'):
                field.widget.attrs.update({'class': field.widget.attrs.get('class', '') + ' mb-3'})

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Leave a comment (optional)...'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your thoughts...'}),
        }

class SongSearchForm(forms.Form):
    search = forms.CharField(
        max_length=200, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search songs, artists, or descriptions...'})
    )
    language = forms.ChoiceField(
        choices=[('', 'All Languages')] + Song.LANGUAGE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    genre = forms.ChoiceField(
        choices=[('', 'All Genres')] + Song.GENRE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('newest', 'Newest First'),
            ('oldest', 'Oldest First'),
            ('highest_rated', 'Highest Rated'),
            ('most_viewed', 'Most Viewed'),
        ],
        initial='newest',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class SongForm(forms.ModelForm):
    """Form for editing song details (metadata only, not files)"""
    class Meta:
        model = Song
        fields = ['title', 'description', 'language', 'genre', 'tags', 'ai_tool_used']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'language': forms.Select(attrs={'class': 'form-select'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.CheckboxSelectMultiple(),
            'ai_tool_used': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if hasattr(field.widget, 'attrs'):
                field.widget.attrs.update({'class': field.widget.attrs.get('class', '') + ' mb-3'})
