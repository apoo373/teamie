import json
import time

weights = {
    'Friends': {
        'Weight': 2.0,
        'FirstLimit': 1000,
        'SecondLimit': 1000000,
    },
    'Influence': {
        'Weight': 4.0,
        'FirstLimit': 1000,
        'SecondLimit': 1000000,
    },
    'Chirpy': {
        'Weight': 4.0,
        'FirstLimit': 1,
        'SecondLimit': 10,
    },
}

Response = {
    "uid": 0,
    "username": "",
    "image": "",
    "fullname": "",
    "counts": {
        "friends_count": 0,
        "followers_count": 0,
        "favourites_count": 0,
        "statuses_count": 0,
    },
    "twubric": {
        "friends": 0,
        "influence": 0,
        "chirpness": 0,
        "total": 0,
    },
    "join_date": "",
    "location": ""
}

def getMetrics(metricsName, value):
    metricData = weights[metricsName]
    print metricData
    if value < metricData["FirstLimit"]:
        return metricData['Weight']*(1.0/3.0)
    elif value >= metricData["FirstLimit"] and value < metricData["SecondLimit"]:
        return metricData['Weight']*(2.0/3.0)
    else:
        return metricData['Weight']*(3.0/3.0)

def ComputeRubric(user_profile_data, user_tweets_data):
    """ This Function Models and Computes the Rubric For Each User, based on the Data Recieved from the Twitter API callself.
    Also format the Data into a specific JSON format"""
    # Start Creating Response
    Response["uid"] = user_profile_data["id"]
    Response["username"] = user_profile_data["screen_name"]
    Response["image"] = user_profile_data["profile_image_url"].replace("normal", "bigger")
    Response["fullname"] = user_profile_data["name"]
    Response["join_date"] = user_profile_data["created_at"]
    Response["location"] = user_profile_data["location"]
    Response["counts"] = {
        "friends_count": user_profile_data["friends_count"],
        "followers_count": user_profile_data["followers_count"],
        "favourites_count": user_profile_data["favourites_count"],
        "statuses_count": user_profile_data["statuses_count"],
    }

    # twubric Metrics
    Response["twubric"]["friends"] = getMetrics('Friends', user_profile_data["friends_count"])
    Response["twubric"]["influence"] = getMetrics('Influence', user_profile_data["followers_count"])
    print Response["twubric"]

    # Compute Avg Tweets Per Day
    tweet_counter = 0.0
    epoch_min = int(time.time())
    for eachTweeet in user_tweets_data:
        tweet_counter = tweet_counter + 1.0
        epochtime = time.mktime(time.strptime(eachTweeet['created_at'],"%a %b %d %H:%M:%S +0000 %Y"))
        epoch_min = min(epoch_min, epochtime)

    time_period = (int(time.time()) - epoch_min) / (60.0 * 60.0 * 24.0) #In days
    avg_tweets_per_day = tweet_counter / time_period
    print avg_tweets_per_day
    Response["twubric"]["chirpness"] = getMetrics('Chirpy', avg_tweets_per_day)

    Response["twubric"]["total"] = Response["twubric"]["friends"] + Response["twubric"]["influence"] + Response["twubric"]["chirpness"]
    return Response
