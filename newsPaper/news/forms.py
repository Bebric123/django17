from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Текст', 'rows': 10}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get("content")
        
        title = cleaned_data.get("title")
        if title == content:
            raise ValidationError(
                "Описание не должно быть идентичным названию."
            )

        return cleaned_data