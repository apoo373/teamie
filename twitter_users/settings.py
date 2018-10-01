
from django.conf import settings

# Required
KEY                  = ''       # Please Enter your App's Key
SECRET               = ''       # Please Enter your App's Secret Key


PROFILE_MODULE       = getattr(settings, 'AUTH_PROFILE_MODULE', 'twitter_users.models.UserProfile')
USERS_FORMAT         = getattr(settings, 'TWITTER_USERS_FORMAT', '%s')

# Login Redirect URl required to be added to your App's twiiter account
LOGIN_REDIRECT_URL   = 'http://127.0.0.1:8000/twitter/allFollowers'
LOGOUT_REDIRECT_URL  = 'http://127.0.0.1:8000/twitter/thanks'


# Usefull twitter urls
TWITTER_URL_ALL_FOLLOWERS = 'https://api.twitter.com/1.1/followers/list.json?skip_status=true&include_user_entities=true'
TWITTER_URL_GET_USER_DETAILS = 'https://api.twitter.com/1.1/users/show.json?user_id='
TWITTER_URL_GET_USER_TWEETS = 'https://api.twitter.com/1.1/statuses/user_timeline.json?count=200&trim_user=true&user_id='
