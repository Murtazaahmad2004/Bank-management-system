import random
import string
import datetime
import MySQLdb
from django import db
from flask import Flask, flash, jsonify, logging, render_template, request, redirect, session, url_for
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bms'

db = MySQLdb.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    passwd=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)

# User Classes
class User:
    def __init__(self, userid, password):
        self.userid = userid
        self.password = password

class Admin(User):
    def __init__(self, userid, password):
        super().__init__(userid, password)

class Employee(User):
    def __init__(self, userid, password):
        super().__init__(userid, password)

# Routes

# Homepage
@app.route('/')
def home():
    return render_template('login_user_employee_auth.html')

# signup
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)