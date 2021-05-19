"""
Main app/routing file for Twitoff
"""
from os import getenv
from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user


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

    @app.route('/populate')
    def populate():
        add_or_update_user("youyanggu")
        add_or_update_user("kareem_carr")
        return render_template("base.html", title="Home", users=User.query.all())

    @app.route('/update')
    def update():
        users = User.query.all()
        for user in users:
            add_or_update_user(username)
        return render_template("base.html", title="Database updated!", users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template("base.html", title="Database reset!", users=User.query.all())

    return app

# TODO: Workflow - Attempt any code at all inside a flask shell, if it works, copy and paste into a function here to make it reproducible. By that logic, use the code Nick writes during Guided Project to figure out how to complete that days Module Project

# TODO: Download old version of twitoff folder with invented data from my github and resubmit for Module 1 Project

# TODO: Already have tweets pulled, need to check SQLite DB Browser to confirm, then edit base.HTML to display tweets underneath users

# TODO: Add vector embeddings for Module 2 Project and then submit

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

