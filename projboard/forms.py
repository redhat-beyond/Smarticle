from django import forms
from .models.article import Article


class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('user_id', 'title', 'subject_id', 'content')
        widgets = {
            'user_id': forms.HiddenInput(),
        }


class EditArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('user_id', 'title', 'subject_id', 'content')
        widgets = {
            'user_id': forms.HiddenInput(),
        }
