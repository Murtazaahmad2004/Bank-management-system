import random
import string
import datetime
import MySQLdb
from flask import Flask, render_template, request, redirect, url_for, session
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.secret_key = '123789456'

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
        
class Customer(User):
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
@app.route('/emp_dashboard/account_manage_entity')
def account_manage_entity():
    return render_template('/emp_dashboard/account_manage_entity.html')

#open acc
@app.route('/emp_dashboard/open_digital_account')
def open_digital_account():
    return render_template('emp_dashboard/open_digital_account.html')

# blocked acc
@app.route('/emp_dashboard/blocked_acc')
def blocked_accounts():
    return render_template('/emp_dashboard/blocked_acc.html')

# crad management
@app.route('/emp_dashboard/card_management')
def card_management():
    return render_template('/emp_dashboard/card_management.html')

#chequebook 
@app.route('/emp_dashboard/chequebook_management')
def chequebook_management():
    return render_template('emp_dashboard/chequebook_management.html')

#Deposite
@app.route('/emp_dashboard/deposit_money')
def deposit_money():
    return render_template('emp_dashboard/deposit_money.html')

# Manager dashboard
@app.route('/manager_dashboard')
def manager_dashboard():
    return render_template('admin_dashboard/manager_dashboard.html')

# user management
@app.route('/user_management')
def user_management():
    return render_template('/admin_dashboard/user_management.html')

# add user
@app.route('/add_user')
def add_user():
    return render_template('/admin_dashboard/add_user.html')

# Login Authentication
@app.route('/login_user_employee_auth', methods=['POST'])
def login_user_employee_auth():
    user_id = request.form.get('userid')
    password = request.form.get('password')

    # Authenticate Employee
    if user_id == "1" and password == "123":
        session['user_id'] = user_id
        session['role'] = 'employee'
        return redirect(url_for('account_manage_entity'))

    # Authenticate Manager (formerly Admin)
    elif user_id == "2" and password == "321":
        session['user_id'] = user_id
        session['role'] = 'manager'
        return redirect(url_for('manager_dashboard'))  # Make sure this route exists

    return "Invalid credentials. Please try again."

# Run the app
if __name__ == '__main__':
    app.run(debug=True)