from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=10)
    class Meta:
        model = Post
        fields = [
            'author',
            'title',
            'text',
            'categoryType',
            'rating',
            'postCategory',

        ]
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        name = cleaned_data.get('name')
        if name == title:
            raise ValidationError(
                'Описание не должно быть идентично названию'
            )

        return cleaned_data