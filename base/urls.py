from django.urls import path
from .views import home, loginPage, do_logout, signin, profile, create_tweet, create_retweet, like_tweet, follow, unfollow, update_profile

urlpatterns = [
    path('', home, name='home'),
    path('login/', loginPage, name='login'),
    path('logout/', do_logout, name='logout'),
    path('signin/', signin, name='signin'),
    path('profile/<str:id>/', profile, name='profile'),
    path('update-profile', update_profile, name='update-profile'),
    path('create-tweet/', create_tweet, name='create-tweet'),
    path('create-retweet/<str:retweet_id>', create_retweet, name='create-retweet'),
    path('like-tweet/<str:tweet_id>', like_tweet, name='like-tweet'),
    path('follow/<str:profile_id>', follow, name='follow'),
    path('unfollow/<str:profile_id>', unfollow, name='unfollow'),
]