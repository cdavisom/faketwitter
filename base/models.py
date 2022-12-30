from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(null=True, default='default_avatar.png')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    follower_list = models.ManyToManyField(User, related_name='follower_list', blank=True)

    def __str__(self) -> str:
        return self.user.username


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    following_list = models.ManyToManyField(User, related_name='following_list', blank=True)

    def __str__(self) -> str:
        return self.user.username

class Topic(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

class Tweet(models.Model):
    message = models.TextField(max_length=280)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True)
    retweet_attached = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, blank=True, null=True)
    
    retweet = models.ManyToManyField(User, related_name='retweet', blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.message[:50]
