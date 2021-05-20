"""
Main app/routing file for Twitoff
"""
from os import getenv
from flask import Flask, render_template, request
from .models import DB, User
from .twitter import add_or_update_user
from .predict import predict_user


def create_app():
    """
    Creates and configures an instance of the flask application
    """
    app = Flask(__name__)   # Name points to where our path is once we run code

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)

    # Decorator provided by Flask, .route is going to run this function when this route is visited
    @app.route('/')
    def root():
        # SQL equivalent = "SELECT * FROM user"
        return render_template("base.html", title="Home", users=User.query.all())

    @app.route('/compare', methods=["POST"])  # An HTTP method
    def compare():
        # Grabbing users and hypothetical tweet from  client
        user0, user1 = sorted(
            [request.values['user0'], request.values['user1']])
        hypo_tweet_text = request.values['tweet_text']

        # Stops clients from comparing same user
        if user0 == user1:
            message = "Cannot compare users to themselves!"

        else:
            prediction = predict_user(user0, user1, hypo_tweet_text)
            message = '"{}" is more likely to be said by {} than {}'.format(
                hypo_tweet_text,
                user1 if prediction else user0,
                user0 if prediction else user1
            )

        return render_template('prediction.html', title='Prediction', message=message)

    # This route will allow us to draw out tweets from any user from Twitter
    @app.route('/user', methods=['POST'])
    # These brackets in user/<name> are provided by Flask
    @app.route('/user/<name>', methods=["GET"])
    def user(name=None, message=''):
        # Manages whether a user is added or updated
        name = name or request.values["user_name"]
        try:
            if request.method == "POST":
                add_or_update_user(name)
                message = f"User {name} successfully added!"

            # Going to print out all the tweets
            tweets = User.query.filter(User.username == name).one().tweets
        except Exception as e:
            message = "Error adding {name}: {e}"
            tweets = []

        return render_template("user.html", title=name, tweets=tweets, message=message)

    @app.route('/populate')
    def populate():
        add_or_update_user("youyanggu")
        add_or_update_user("kareem_carr")
        return render_template("base.html", title="Home", users=User.query.all())

    @app.route('/update')
    def update():
        users = User.query.all()
        for user in users:
            add_or_update_user(user.username)
        return render_template("base.html", title="Database updated!", users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="Database reset!", users=User.query.all())

    return app

# TODO: Workflow - Attempt any code at all inside a flask shell, if it works, copy and paste into a function here to make it reproducible.

# def insert_users(usernames):
#     for id_index, username in enumerate(usernames):
#         user = User(id=id_index, username=username)
#         DB.session.add(user)
#         DB.session.commit()


# def insert_tweets(tweets, user):
#     for index in range(6):
#         tweet_ = Tweet(
#             id=index+1, text=tweets[index], user=User.query.filter_by(username=f'NegarestaniReza').first())
#         # TODO: Read up on the SQLalchemy documentation in order to assign my six invented tweets to not just one user, but BOTH: https://docs.sqlalchemy.org/en/14/orm/query.html?highlight=filter_by#sqlalchemy.orm.Query.filter_by
#         DB.session.add(tweet_)
#         DB.session.commit()
