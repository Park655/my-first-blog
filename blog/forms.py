from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='아이디', max_length=150)
    first_name = forms.CharField(label='이름', max_length=30)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']  # 👈 이름 저장!
        if commit:
            user.save()
        return user


