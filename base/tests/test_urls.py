from django.test import SimpleTestCase
from django.urls import reverse, resolve
from base.views import home, profile

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)
    
    def test_profile_url_is_resolved(self):
        url = reverse('profile', args=['1'])
        self.assertEqual(resolve(url).func, profile)