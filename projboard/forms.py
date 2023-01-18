from django import forms
from .models.article import Article
from projboard.models.user import User


class CreateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('user_id', 'title', 'subject_id', 'content')
        widgets = {
            'user_id': forms.HiddenInput(),
        }


class NewUserForm(forms.ModelForm):
    """STILL NEED TO ADD PASSWORD1 PASSWORD2 TO CONFIRM"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'example@example.com'}))
    name = forms.CharField(required=True, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Name'}))
    nickname = forms.CharField(required=True, widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Nickname'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password_confirm = forms.CharField(required=True, widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['email', 'name', 'nickname', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")


class EditArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('user_id', 'title', 'subject_id', 'content')
        widgets = {
            'user_id': forms.HiddenInput(),
        }
