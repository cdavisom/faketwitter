from django.test import TestCase
from base.forms import TweetFrom
from base.models import Topic

class TestForms(TestCase):

    def test_tweet_form_with_valid_data(self):
        topic = Topic.objects.create(name="randon")

        form = TweetFrom(data={
            'message': 'new message',
            'topic': topic
        }, files={'image': ''})
        self.assertTrue(form.is_valid())
    
    def test_tweet_form_with_no_data(self):
        form = TweetFrom(data={})
        self.assertFalse(form.is_valid())