import random
import string
import MySQLdb
from flask import Flask, render_template, request, jsonify
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
    def generate_random_id(length=5):
        """Generate a random numeric ID of specified length."""
        return ''.join(random.choices(string.digits, k=length))

# For GET request, pre-generate random IDs
    user_id = generate_random_id()
    return render_template('signup.html', user_id=user_id)

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
    def generate_random_id(length=5):
        return ''.join(random.choices(string.digits, k=length))

    def generate_random_acct_no(length=9):
        return ''.join(random.choices(string.digits, k=length))

    # Generate the random IDs
    customer_id = generate_random_id()
    acct_no = generate_random_acct_no()

    return render_template('emp_dashboard/open_digital_account.html', customer_id=customer_id, acct_no=acct_no)

# blocked acc
@app.route('/emp_dashboard/blocked_acc')
def blocked_accounts():
    return render_template('/emp_dashboard/blocked_acc.html')

# card management
@app.route('/emp_dashboard/card_management')
def card_management():
    def generate_random_card_no(length=16):
        return ''.join(random.choices(string.digits, k=length))

    def generate_random_cvv(length=3):
        return ''.join(random.choices(string.digits, k=length))
    
    def generate_random_id(length=5):
        return ''.join(random.choices(string.digits, k=length))

    # Generate the random IDs
    card_no = generate_random_card_no()
    cvv = generate_random_cvv()
    custm_id = generate_random_id()

    return render_template('emp_dashboard/card_management.html', card_no=card_no, cvv=cvv, custm_id=custm_id)

#chequebook 
@app.route('/emp_dashboard/chequebook_management')
def chequebook_management():
        def generate_random_id(length=5):
            return ''.join(random.choices(string.digits, k=length))
        
        customer_id = generate_random_id()
        return render_template('emp_dashboard/chequebook_management.html', customer_id=customer_id)

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
    return render_template('admin_dashboard/user_management.html')

# add user
@app.route('/add_user')
def add_user():
    def generate_random_id(length=5):
        return ''.join(random.choices(string.digits, k=length))
    
    # Generate the random IDs
    user_id = generate_random_id()

    return render_template('admin_dashboard/add_user.html', user_id=user_id)

# Set Transaction Limits
@app.route('/set_transaction_limits')
def set_transaction_limits():
    def generate_random_id(length=5):
        return ''.join(random.choices(string.digits, k=length))
    
    # Generate the random IDs
    user_id = generate_random_id()
    return render_template('emp_dashboard/set_transaction_limits.html', user_id=user_id)

#loan management
@app.route('/loan_management')
def loan_management():
    return render_template('/admin_dashboard/loan_management.html')

# loan application
@app.route('/loan_application')
def loan_application():
    def generate_random_id(length=5):
        return ''.join(random.choices(string.digits, k=length))
    
    # Generate the random IDs
    cust_id = generate_random_id()
    return render_template('admin_dashboard/loan_application.html', cust_id=cust_id)

# loan repay
@app.route('/loan_repay')
def loan_repay():
    return render_template('/admin_dashboard/loan_repay.html')

# report
@app.route('/reports')
def report():
    return render_template('/cust_dashboard/reports.html')

# balance
@app.route('/balance')
def balance():
    return render_template('/admin_dashboard/balance.html')

# customer dashboard
@app.route('/customer_dashboard')
def customer_dashboard():
    return render_template('/cust_dashboard/customer_dashboard.html')

# customer profile
@app.route('/customer_profile')
def customer_profile():
    return render_template('/cust_dashboard/customer_profile.html')

# account info
@app.route('/account_info')
def account_info():
    return render_template('/cust_dashboard/account_info.html')

#loan details
@app.route('/loan_detail')
def loan_detail():
    return render_template('/cust_dashboard/loan_detail.html')

# card mang
@app.route('/card_mang')
def card_mang():
    return render_template('/cust_dashboard/card_mang.html')

# Route to Get Total Balance from Deposit Table
@app.route('/get_balance', methods=['GET'])
def get_balance():
    cursor = db.cursor()
    cursor.execute("SELECT SUM(amount) AS total_balance FROM deposit")  # Adjust table name if needed
    result = cursor.fetchone()
    total_balance = result['total_balance'] if result['total_balance'] else 0  # Handle NULL case
    return jsonify({'balance': total_balance})

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

    # Authenticate Customer
    elif user_id == "3" and password == "124":
        session['user_id'] = user_id
        session['role'] = 'manager'
        return redirect(url_for('customer_dashboard'))  # Make sure this route exists
    
    return "Invalid credentials. Please try again."

# # fetch customer data
# @app.route('/customer_profile_data', methods=['GET', 'POST'])
# def customer_profile_data():
#     if request.method == 'POST':
#         # Get the patient ID from the form
#         phone_no = request.form.get('phone_no')

#         # Validate the input
#         if not phone_no:
#             return render_template('customer_profile_data.html', error="Phone No is required!")

#         # Fetch the customer_data from the database
#         cursor = db.cursor()
#         try:
#             cursor.execute("""
#                 SELECT * FROM customer_profile WHERE phone_no = %s
#             """, (phone_no,))
#             customer_data = cursor.fetchall()  # Use fetchall to get all records

#             if customer_data:
#                 customer_list = []
#                 for data in customer_data:
#                     customer_dict = {
#                         'Customer ID': data[1],
#                         'First_Name': data[2],
#                         'Last_Name': data[3],
#                         'Email': data[4],
#                         'Phone_No': data[5],
#                         'Date_of_Birth': data[6],
#                         'Account_Type': data[7],
#                     }
#                     customer_list.append(customer_dict)
#                 return render_template('customer_profile_data.html', customer_list=customer_list)

#             else:
#                 return render_template('customer_profile_data.html', error="No customer record found for this Phonr No.")

#         except Exception as e:
#             error = f"Failed to fetch Customer Data. Error: {str(e)}"
#             print(error)  # Log the error for debugging
#             return render_template('customer_profile_data.html', error=error)

#         finally:
#             cursor.close()

#     # Render the form for GET request
#     return render_template('customer_profile_data.html')

# fetch account data
# @app.route('/account_info_data', methods=['GET', 'POST'])
# def account_info_data():
#     if request.method == 'POST':
#         # Get the patient ID from the form
#         account_no = request.form.get('account_no')

#         # Validate the input
#         if not account_no:
#             return render_template('account_info_data.html', error="Account No is required!")

#         # Fetch the account_data from the database
#         cursor = db.cursor()
#         try:
#             cursor.execute("""
#                 SELECT * FROM account_info_data WHERE account_no = %s
#             """, (account_no,))
#             account_data = cursor.fetchall()  # Use fetchall to get all records

#             if account_data:
#                 account_list = []
#                 for data in account_data:
#                     account_dict = {
#                         'Customer ID': data[1],
#                         'First_Name': data[2],
#                         'Last_Name': data[3],
#                         'Email': data[4],
#                         'Phone_No': data[5],
#                         'Date_of_Birth': data[6],
#                         'Account_Type': data[7],
#                     }
#                     account_list.append(account_dict)
#                 return render_template('account_info_data.html', account_list=account_list)

#             else:
#                 return render_template('account_info_data.html', error="No customer record found for this Phonr No.")

#         except Exception as e:
#             error = f"Failed to fetch Account Data. Error: {str(e)}"
#             print(error)  # Log the error for debugging
#             return render_template('account_info_data.html', error=error)

#         finally:
#             cursor.close()

#     # Render the form for GET request
#     return render_template('account_info_data.html')

# Run the app
if __name__ == '__main__':
    app.run(debug=True)