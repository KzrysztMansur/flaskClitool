#!/usr/bin/python3
import click
import os
"""
THIS IS A SCRIPT TO CREATE PYTHON FLASK-REACT APP TEMPLATES


"""

class Webapp:
    def __init__(self, project_name):
        self.project_name = project_name
        self._db = False

    def add_db(self, db_type):
        self._db = True
        self.db_type = db_type
        return self
    
    
    def create(self):
        self.create_run()

        os.mkdir(self.project_name)
        os.chdir(self.project_name)

        if (self._db):
            if (self.db_type == 'sql'):
                self.create_sql_db_connection()
            elif (self.db_type == 'mongo'):  
                self.create_mongo_db_connection()
            else:
                raise Exception("not in db list try flaskapp --help to get more info")
        else:            
            self.create_no_db_connection()

        self.create_routes()

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
    <h1>{{ msg }}</h1>
</body>
</html>

            """)

        os.chdir("..")
        os.mkdir("static")

        os.chdir("..")
        os.chdir("..")

        click.echo(f"Flask app created at: {os.getcwd()}/{self.project_name}")


    def create_run(self):
        with open('run.py', 'w') as f:
            f.write(f"""from {self.project_name} import app

if __name__ == '__main__':
    app.run(debug=True, port=5000)

                """)

    def create_sql_db_connection(self):
        with open('models.py', 'w') as f:
            f.write("""from app import app
from sqlalchemy import Column, Integer, String, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    # Relationships
    posts = relationship('Post', backref='author', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Post(db.Model):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(1000), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)       

    def __init__(self, title, content, user_id):
        self.name = name
        self.amount = amount
        self.arrival_date = arrival_date
        self.user_id = user_id

                """)

        with open('__init__.py', 'w') as f:
            f.write(f"""from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = ''
app.config['ENV'] = 'production'



from .models import db
from .routes import *
                
                """)  

    def create_mongo_db_connection(self):
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

        with open('__init__.py', 'w') as f: # Create a __init__.py file with the connection to a mongo db database
            f.write(f"""from flask import Flask
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("localhost", 27017) #instead of the localhost write your db connection

db = client.test1


from .routes import *
                
                """)


    def create_no_db_connection(self): # Create a normal __init__.py with no database connections
        with open('__init__.py', 'w') as f:
            f.write(f"""from flask import Flask

app = Flask(__name__)

from .routes import *
                """)

     
    def create_routes(self):
        with open('routes.py', 'w') as f:
            f.write("""from flask import redirect, url_for, render_template, request
from .__init__ import app
                        
@app.route('/', methods=['GET','POST'])
def home():
    msg = 'App template'
    if request.method=='POST':
        # Handle POST Request here
        
        
        return render_template('index.html', msg=msg)         


    return render_template('index.html', msg=msg)         

            """)


@click.command()
@click.option("-name", is_flag=False, flag_value="Flag", default="app", type=str)
@click.option('-db', required=False, default= None, type=str)
def main(name, db):
    flaskapp = Webapp(name)
    if (db is not None):
        flaskapp.add_db(db)


    flaskapp.create()



if __name__ == '__main__':
    main()