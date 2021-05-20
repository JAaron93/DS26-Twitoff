"""Handle connection to Twitter Database"""
from os import getenv
from .models import DB, Tweet, User
import spacy
import tweepy

# Authenticates me and allows me to use Twitter's API
# We use .env files to assign our api & secret api keys to these variables below. Our .gitignore won't push it to GitHub.
# This obscures our API access(or login info) from being visible to would-be hackers
TWITTER_API_KEY = getenv("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = getenv("TWITTER_API_KEY_SECRET")
# This method will send a request to Twitter's API with our key & secret key(username & password) and returns an authentication object.
# This authentication object will confirm if our keys are correct are not. It essentially validates a login, allowing us access to Twitter's data.
TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
api = tweepy.API(TWITTER_AUTH)


# NLP model
nlp = spacy.load("my_model")


# Creating function to vectorize tweet
# Vectorization is the process of converting an algorithm from operating on a single value at a time to operating on a set of values at one time.
def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    """
    Takes a username and adds them to our DB from the twitter DB.
    Get user and get up to 200 of their tweets and add to our
    SQLAlchemy database.
    """
    # Error handling
    # How do we deal with the possibility of getting a user that doesn't exist?
    # Will break our code! We can handle that by using a try statement!
    try:
        twitter_user = api.get_user(username)
        # Where we decide whether or not to add or update.
        # By prefacing code with a db, that means we're adding it to our database
        # .get will be grabbing our twitter users by their id. If that user is in our database? Grab that user and assign it to db_user.
        # If that user isn't in our database, it'll go with the second argument where it will CREATE a user
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, username=username)

        DB.session.add(db_user)

        # TODO: grab same number of tweets for each user. Use tweepy documentation to figure this out with pre-filtering to counter the current post-filtering we have written here
        tweets = twitter_user.timeline(
            count=200,
            exclude_replies=True,
            include_rts=False,
            # Returns everything about a tweet, including emojis or whatever else
            tweet_mode="extended",
            since_id=db_user.newest_tweet_id   # This is where the updating happens
        )

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            # Run vectorize_tweet function
            tweet_vector = vectorize_tweet(tweet.full_text)
            # Creating a Tweet object to add to our DB
            db_tweet = Tweet(
                id=tweet.id, text=tweet.full_text, vect=tweet_vector)
            # Connects the tweet to the user through this tweets list (user.tweets)
            # SQLAlchemy will make that connection between user and tweets
            db_user.tweets.append(db_tweet)
            # Note: If we added before appending we would likely get an error
            DB.session.add(db_tweet)

    except Exception as e:
        # This will be returned as the reason the non-existent user cannot be added
        print(f"Error Processing {username}: {e}")
        raise e

    else:
        DB.session.commit()
