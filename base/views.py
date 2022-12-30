import random
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Following, Followers, Tweet, Topic
from .forms import TweetFrom, CustomUserCreationForm, UserForm

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        get_object_or_404(User, email=email)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    
    return render(request, 'identification/login.html')

def do_logout(request):
    logout(request)
    return redirect('login')

def signin(request):
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            Following.objects.create(user=user)
            Followers.objects.create(user=user)
            login(request, user)
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'identification/signin.html', context)

@login_required(login_url='login')
def home(request):
    following, _ = Following.objects.get_or_create(user = request.user)
    following = following.following_list.all()
    followers, _ = Followers.objects.get_or_create(user = request.user)
    followers = followers.follower_list.all()
    
    tweets = []
    for fol in following:
        tweets.extend([ tweet for tweet in Tweet.objects.filter(author=fol).order_by('-created')] )
    random.shuffle(tweets)
    
    explore_profiles = User.objects.filter(~Q(id__in=([f.id for f in following] + [request.user.id]))).order_by('-date_joined')

    context = {'following': following[:10], 'followers': followers[:10], 'explore_profiles': explore_profiles, 'tweets': tweets}
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def profile(request, id):
    user = get_object_or_404(User, id=id)
    following = Following.objects.get(user__id = id).following_list.all()
    followers = Followers.objects.get(user__id = id).follower_list.all()

    tweets = Tweet.objects.filter( Q(author__id=id) | Q(retweet__id=id) | Q(likes__id=id)).order_by('-updated')

    explore_profiles = User.objects.filter(~Q(id__in=([f.id for f in following] + [request.user.id]))).order_by('-date_joined')
    
    context = {'profile': user, 'following': following, 'followers': followers, 'explore_profiles': explore_profiles, 'tweets': tweets}
    
    return render(request, 'profile/profile.html', context)

@login_required(login_url='login')
def update_profile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', id=request.user.id)

    context = {'form': form}
    return render(request, 'profile/update_profile.html', context)

@login_required(login_url='login')
def create_tweet(request):
    form = TweetFrom()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, _ = Topic.objects.get_or_create(name=topic_name)
        image = request.FILES.get('image') if request.FILES.get('image') else None
        Tweet.objects.create(
            message = request.POST.get('message'),
            author = request.user,
            topic = topic,
            image = image
            )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/create_tweet.html', context)

@login_required(login_url='login')
def create_retweet(request, retweet_id):
    form = TweetFrom()
    topics = Topic.objects.all()
    retweet = get_object_or_404(Tweet, id=retweet_id)
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, _ = Topic.objects.get_or_create(name=topic_name)
        Tweet.objects.create(
            message = request.POST.get('message'),
            author = request.user,
            topic = topic,
            retweet_attached = retweet,
            )
        return redirect('home')

    context = {'form': form, 'topics': topics, 'retweet': retweet}
    return render(request, 'base/retweet.html', context)

@login_required(login_url='login')
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.user not in tweet.likes.all():
        tweet.likes.add(request.user)
    else:
        tweet.likes.remove(request.user)
    return redirect('home')

@login_required(login_url='login')
def follow(request, profile_id):
    idol = get_object_or_404(User, id=profile_id)
    followers = get_object_or_404(Followers, user__id=idol.id)
    followers.follower_list.add(request.user)
    
    following = get_object_or_404(Following, user__id=request.user.id)
    following.following_list.add(idol)
    return redirect('profile', id=profile_id)

@login_required(login_url='login')
def unfollow(request, profile_id):
    idol = get_object_or_404(User, id=profile_id)
    followers = get_object_or_404(Followers, user__id=idol.id)
    followers.follower_list.remove(request.user)
    
    following = get_object_or_404(Following, user__id=request.user.id)
    following.following_list.remove(idol)
    return redirect('profile', id=request.user.id)