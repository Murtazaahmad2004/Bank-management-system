import random
import string
import datetime
import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, session
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

# Homepage (Login Form)
@app.route('/')
def home():
    return render_template('login_user_employee_auth.html')

# Signup Page
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Logout 
@app.route('/login_user_employee_auth')
def logout():
    return redirect(url_for('home'))

# Account Management Page
@app.route('/account_manage_entity')
def account_manage_entity():
    return render_template('account_manage_entity.html')

# Login
@app.route('/login_user_employee_auth', methods=['POST'])
def login_user_employee_auth():
    user_id = request.form.get('userid')
    password = request.form.get('password')

    # Authenticate User
    if user_id == "1" and password == "123":
        return redirect(url_for('account_manage_entity'))  # Redirect if credentials are correct
    else:
        return "Invalid credentials. Please try again."

#open acc
@app.route('/open_digital_account')
def open_digital_account():
    return render_template('open_digital_account.html')

# blocked acc
@app.route('/blocked_acc')
def blocked_accounts():
    return render_template('blocked_acc.html')

# crad management
@app.route('/card_management')
def card_management():
    return render_template('card_management.html')

#chequebook 
@app.route('/chequebook_management')
def chequebook_management():
    return render_template('chequebook_management.html')

#Deposite
@app.route('/deposit_money')
def deposit_money():
    return render_template('deposit_money.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)