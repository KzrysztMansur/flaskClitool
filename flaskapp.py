#!/usr/bin/python3
import click
import os
"""
THIS IS A SCRIPT TO CREATE PYTHON FLASK-REACT APP TEMPLATES


"""

class Webapp:
    def __init__(self, project_name):
        self.project_name = project_name
        self._db = None

    def add_auth(self):
        self._auth = True
        return self

    def add_db(self, db_type):
        self._db = True
        self.db_type = db_type
        return self
    
    def create(self):
        with open('run.py', 'w') as f:
            f.write(f"""from {self.project_name} import app

if __name__ == '__main__':
    app.run(debug=True, port=5000)

            """)

        os.mkdir(self.project_name)
        os.chdir(self.project_name)

        if (self.db_type == 'sql'):

            with open('__init__.py', 'w') as f:
                f.write(f"""from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
                
from . import models

from .views import *

                """)  
            
            with open('models.py', 'w') as f:
                f.write("""from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from . import db  # Assuming db is the SQLAlchemy instance created in __init__.py

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    # Relationships
    posts = relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(1000), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)       

                """)
        elif (self.db_type == 'mongo'):
            with open('__init__.py', 'w') as f:
                f.write(f"""from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/your_database'

mongoDB = PyMongo(app)

from . import mongo_models

from .views import *
                """)
            with open('models.py', 'w') as f:
                f.write("""from flaskapp import mongo

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @staticmethod
    def get_user_by_username(username):
        return mongo.db.users.find_one({'username': username})

    def save(self):
        mongo.db.users.insert_one({
            'username': self.username,
            'password': self.password,
            'email': self.email
        })

class Post:
    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

    @staticmethod
    def get_posts_by_user_id(user_id):
        return mongo.db.posts.find({'user_id': user_id})

    def save(self):
        mongo.db.posts.insert_one({
            'title': self.title,
            'content': self.content,
            'user_id': self.user_id
        })
                """)

        else:
            
            with open('__init__.py', 'w') as f:
                f.write(f"""from flask import Flask

app = Flask(__name__)

from .views import *

                """)  
        
        with open('views.py', 'w') as f:
            f.write("""from flask import redirect, url_for, render_template, request
from .__init__ import app
                        
@app.route('/', methods=['GET','POST'])
def home():
    if request.method=='POST':
        # Handle POST Request here
        return render_template('index.html')
        msg = 'data'
        return render_template('index.html', msg=msg)         


    return render_template('index.html')         

            """)


        os.mkdir("templates")
        os.chdir("templates")

        with open('index.html', 'w') as f:
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    {{msg}}
</body>
</html>

            """)

        os.chdir("..")
        os.mkdir("static")

        os.chdir("..")
        os.chdir("..")

        click.echo(f"Flask app created at: {os.getcwd()}/{self.project_name}")


@click.command()
@click.option("-name", is_flag=False, flag_value="Flag", default="flaskapp", type=str)
@click.option('-db', required=False, default= None)
def main(name, db):
    flaskapp = Webapp(name)
    if (db is not None):
        flaskapp.add_db(db)


    flaskapp.create()



if __name__ == '__main__':
    main()