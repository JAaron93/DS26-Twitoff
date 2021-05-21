"""SQLAlchemy models and database architecture"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


# Creates a 'user' Table
class User(DB.Model):
    '''
    Twitter users that we'll pull & analyze tweets for
    '''
    # id primary key column for 'user'
    id = DB.Column(DB.BigInteger, primary_key=True)
    # username column for 'user'
    username = DB.Column(DB.String, nullable=False)
    # stores most recent tweet_id
    newest_tweet_id = DB.Column(DB.BigInteger)

    # Representation of our object
    def __repr__(self):
        return f"<User: {self.username}>"


# Creates a 'tweet' Table
class Tweet(DB.Model):
    '''
    The Tweets themselves
    '''
    # id primary key column for 'tweet'
    id = DB.Column(DB.BigInteger, primary_key=True)
    # text column for 'tweet'
    # Also make sure to use UNICODE b/c emojis and the like
    text = DB.Column(DB.Unicode(600))
    # Creating a new column for vectorization
    # Being saved as a pickletype to deal with numpy arrays generated from the NLP we ran with Spacy & word2vect in our twitter.py
    # Stores numbers that represent tweets
    vect = DB.Column(DB.PickleType, nullable=False)
    # user_id foreign key column for 'tweet'
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))
    # backref allows us to populate the tweets without performing an explicit join

    def __repr__(self):
        return f"<Tweet: {self.text}>"
