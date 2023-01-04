from django.test import TestCase, Client
from django.urls import reverse
from base.models import User, Tweet, Followers, Following
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.profile_url = reverse('profile', args=['1'])
        self.create_tweet_url = reverse('create-tweet')

        self.user = User.objects.create_user(email='test@email.com', username='test', password='test')
        Followers.objects.create(user=self.user)
        Following.objects.create(user=self.user)
        self.client.login(email='test@email.com', password='test')

    def test_home_logged_GET(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/home.html')

    def test_home_not_logged_GET(self):
        self.client.logout()
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 302)

    def test_profile_logged_GET(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/profile.html')
    
    def test_create_tweet_POST(self):
        response = self.client.post(self.create_tweet_url, {
            'message': 'Random message',
            'topic': 'Random',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Tweet.objects.first().topic.name, 'Random')
        self.assertEqual(Tweet.objects.first().message, 'Random message')
