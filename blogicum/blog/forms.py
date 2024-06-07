from django import forms

from .models import Post, Comments


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}
            )
        }


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': '5', 'cols': '20'}),
        }
