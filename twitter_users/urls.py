from django.conf.urls import url
from twitter_users import views

urlpatterns = [
    url(r'^login/?$',           views.twitter_login,    name='twitter-login'),
    url(r'^allFollowers/?$',           views.twitter_followers,    name='twitter-followers'),
    url(r'^login/callback/?$',  views.twitter_callback, name='twitter-callback'),
    url(r'^logout/?$',          views.twitter_logout,   name='twitter-logout'),
    url(r'^followerAnalysis/(?P<user_id>\w+)?$',           views.twitter_follower_analysis,    name='twitter-follower-analysis'),
    url(r'^thanks/?$',          views.thanks,   name='thanks'),
]
