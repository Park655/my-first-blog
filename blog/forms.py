from django import forms
from .models import Post
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import SelectDateWidget
import datetime

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='아이디', max_length=150)
    first_name = forms.CharField(label='이름', max_length=30)
    gender = forms.ChoiceField(label='성별', choices=UserProfile.GENDER_CHOICES)
    birthdate = forms.DateField(
        label='생년월일',
        widget=SelectDateWidget(
            years=range(datetime.date.today().year, 1900, -1)
        )
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'password1', 'password2', 'gender', 'birthdate']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
            UserProfile.objects.create(
            user=user,
            gender=self.cleaned_data['gender'],
            birthdate=self.cleaned_data['birthdate'],
        )
        return user