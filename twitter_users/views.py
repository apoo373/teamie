
import re
import json
import requests
import requests_oauthlib

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, NoReverseMatch
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout

from twitter_users import oauth, rubric, settings

def is_safe_redirect(redirect_to):
    if ' ' in redirect_to:
        return False
    # exclude http://foo.com URLs, but not paths with GET parameters that
    # have URLs in them (/?foo=http://foo.com)
    #elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
    #    return False
    return True

def twitter_login(request, redirect_field_name='next'):
    # construct the callback URL
    try:
        protocol      = 'https' if request.is_secure() else 'http'
        host          = request.get_host()
        path          = reverse('twitter-callback')
        callback_url  = protocol + '://' + host + path
    except NoReverseMatch:
        callback_url  = None

    # get a request token from Twitter
    consumer      = oauth.Consumer(settings.KEY, settings.SECRET)
    request_token = oauth.RequestToken(consumer, callback_url=callback_url)

    # redirect to Twitter for authorization
    return HttpResponseRedirect(request_token.authorization_url)

def twitter_callback(request):
    oauth_token    = request.GET['oauth_token']
    oauth_verifier = request.GET['oauth_verifier']

    # get an access token from Twitter
    consumer           = oauth.Consumer(settings.KEY, settings.SECRET)
    access_token       = oauth.AccessToken(consumer, oauth_token, oauth_verifier)

    # actually log in
    user = authenticate(twitter_id  = access_token.user_id,
                        username    = access_token.username,
                        token       = access_token.token,
                        secret      = access_token.secret)
    login(request, user)

    # Store the user keys in session
    request.session['access_token'] = json.dumps(
        {
            'twitter_id': access_token.user_id,
            'username': access_token.username,
            'token': access_token.token,
            'secret': access_token.secret
        })

    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

# Send the List of Twitter Followers
def twitter_followers(request):
    user_access_token = json.loads(request.session['access_token'])
    oauth1_authentication = requests_oauthlib.OAuth1(settings.KEY, settings.SECRET, user_access_token['token'], user_access_token['secret'])
    response = requests.get(settings.TWITTER_URL_ALL_FOLLOWERS, auth=oauth1_authentication).json()
    #return HttpResponse(response)
    return render(request, 'twitter_users/allFollowers.html', {'followers': response['users']})

# Single User Analysis
def twitter_follower_analysis(request, user_id):
    user_access_token = json.loads(request.session['access_token'])
    oauth1_authentication = requests_oauthlib.OAuth1(settings.KEY, settings.SECRET, user_access_token['token'], user_access_token['secret'])
    # Get User Profile
    user_profile = requests.get(settings.TWITTER_URL_GET_USER_DETAILS + user_id, auth=oauth1_authentication).json()
    user_tweets = requests.get(settings.TWITTER_URL_GET_USER_TWEETS + user_id, auth=oauth1_authentication).json()
    user_analysis = rubric.ComputeRubric(user_profile, user_tweets)
    print user_analysis
    #return JsonResponse(user_analysis)
    return render(request, 'twitter_users/userAnalysis.html', {'user': user_analysis})

def twitter_logout(request, redirect_field_name='next'):
    if request.user.is_authenticated():
        # get the redirect destination
        redirect_to = settings.LOGOUT_REDIRECT_URL
        logout(request)
    else:
        redirect_to = '/'

    return HttpResponseRedirect(redirect_to)


# thanks
def thanks(request):
    return HttpResponse('You Have Been Logged out !!')
