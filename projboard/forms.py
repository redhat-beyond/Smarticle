from django import forms
from .models.article import Article


class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('user_id', 'title', 'subject_id', 'content')
        widgets = {
            'user_id': forms.HiddenInput(),
        }


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
