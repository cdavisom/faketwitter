from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Tweet, User

class TweetFrom(ModelForm):
    class Meta:
        model = Tweet
        fields = '__all__'
        exclude = ['author', 'retweet_attached', 'likes', 'retweet']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name', 'bio']