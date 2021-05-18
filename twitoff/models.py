"""SQLAlchemy models and database architecture"""

from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


# Creates a 'user' Table
class User(DB.Model):
    # id primary key column for 'user'
    id = DB.Column(DB.BigInteger, primary_key=True)
    # username column for 'user'
    username = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return f"<User: {self.username}>"


# Creates a 'tweet' Table
class Tweet(DB.Model):
    # id primary key column for 'tweet'
    id = DB.Column(DB.BigInteger, primary_key=True)
    # text column for 'tweet'
    text = DB.Column(DB.Unicode(300))
    # user_id foreign key column for 'tweet'
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)

    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f"<Tweet: {self.text}>"


def insert_example_user():
    """Will receive error if ran twice since data already exists"""
    negarestanireza = User(id=1, name="NegarestaniReza")
    youyanggu = User(id=2, name="youyanggu")
    DB.session.add(negarestanireza)  # Adds NegarestaniReza user
    DB.session.add(youyanggu)  # Adds youyanggu user
    DB.session.commit()


def insert_example_tweet(count=6):
    """Will receive error if ran twice since data already exists"""
    tweets = []

    tweet_text = ["Among the greatest critics of logical empiricism, among others.",
                  "The fact that a lot of great engineers who have become philosophers and theorists now prefer to be identified as scientists tells a lot about the current state of philosophy: You can only defend philosophy by resorting to scientific authority.",
                  "The worst thing about the meme economy is that some oedipal brat baby boy with multimillion Twitter followers & the capacity to bring his mommy on SNL can swing this sector of finance this way or that way. And some people feel grateful about that. If that's reality, short&distort",
                  "Due to reporting lag, current all-cause deaths are not available for several weeks. Hence, I used historical data to estimate this for each state.",
                  "The end of an iconic duo: Covid and masks.",
                  "I estimate that US as a whole is currently seeing ~58,400 all-cause deaths a week. The upper bound for excess deaths is ~56,000, so the percent excess is around 4% or 350 deaths per day. As much as we'd like to think that the pandemic is over, unfortunately that's not true yet."]
    while count > 0:
        id = count
        text = random.choice(tweet_text)
        user_id = random.randint(1, 2)

        tweet = Tweet(id=id, text=text, user_id=user_id)
        tweets.append(tweet)
        count -= 1

    DB.session.add_all(tweets)
    DB.session.commit()
