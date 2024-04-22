#!/usr/bin/python3
import click
import os
"""
THIS IS A SCRIPT TO CREATE PYTHON FLASK-REACT APP TEMPLATES


"""

class Webapp:
    def __init__(self, project_name):
        self.project_name = project_name

    def add_auth(self):
        self._auth = True
        return self

    def add_db(self):
        self._db = True
        return self
    
    def create(self):
        with open('run.py', 'w') as f:
            f.write(f"""from {self.project_name} import app

if _name_ == '__main__':
    app.run(debug=True, port=5000)

            """)

        os.mkdir(self.project_name)
        os.chdir(self.project_name)

        if (self._db):

            with open('_init_.py', 'w') as f:
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
from . import db  # Assuming db is the SQLAlchemy instance created in _init_.py

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

        else:
            
            with open('_init_.py', 'w') as f:
                f.write(f"""from flask import Flask

app = Flask(__name__)

from .views import *

                """)  
        
        with open('views.py', 'w') as f:
            f.write("""from flask import redirect, url_for, render_template, request
from ._init_ import app
                        
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
@click.option('-db', required=False, default= False)
def main(name, db):
    flaskapp = Webapp(name)
    if (db):
        flaskapp.add_db()

    flaskapp.create()



if __name__ == '__main__':
    main()
    
