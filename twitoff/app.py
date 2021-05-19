"""
Main app/routing file for Twitoff
"""
# from os import getenv
from flask import Flask, render_template
from .models import DB, User, Tweet
# from .twitter import add_or_update_user


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
        return render_template("base.html", title="Home", users=User.query.all())

    @app.route('/populate')
    def populate():
        insert_users(["kareem_carr", "NegarestaniReza"])
        insert_tweets([
            "What will come next.",
            "Among the greatest critics of logical empiricism, among others.",
            "You can only defend philosophy by resorting to scientific authority.",
            "Being a philosopher coincides with the fact that u are in debt to all philosophers who have excited you and made a philosopher out of u.",
            "Be afraid, very afraid.",
            "Korean translation of Cyclonopedia. All my thanks to Mediabus:"
        ],
            user=["kareem_carr", "NegarestaniReza"])
        return render_template("base.html", title="Home", users=User.query.all())

        @app.route('/reset')
        def reset():
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="Home", User.query.all())

    return app


def insert_users(usernames):
    for id_index, username in enumerate(usernames):
        user = User(id=id_index, username=username)
        DB.session.add(user)
        DB.session.commit()


def insert_tweets(tweets, user):
    for index in range(6):
        tweet_ = Tweet(
            id=index+1, text=tweets[index], user=User.query.filter_by(username=f'NegarestaniReza').first())
        # TODO: Read up on the SQLalchemy documentation in order to assign my six invented tweets to not just one user, but BOTH: https://docs.sqlalchemy.org/en/14/orm/query.html?highlight=filter_by#sqlalchemy.orm.Query.filter_by
        DB.session.add(tweet_)
        DB.session.commit()
