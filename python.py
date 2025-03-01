import random
import string
import MySQLdb
from flask import Flask, flash, render_template, request, jsonify
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

# Logout 
@app.route('/login_user_employee_auth')
def logout():
    return redirect(url_for('home'))

# Account Management Page
@app.route('/emp_dashboard/account_manage_entity')
def account_manage_entity():
    return render_template('/emp_dashboard/account_manage_entity.html')

# blocked acc
@app.route('/emp_dashboard/blocked_acc')
def blocked_accounts():
    return render_template('/emp_dashboard/blocked_acc.html')

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

#loan management
@app.route('/loan_management')
def loan_management():
    return render_template('/admin_dashboard/loan_management.html')

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

# Signup Page
@app.route('/signup')
def signup():
    def generate_random_id(length=5):
        """Generate a random numeric ID of specified length."""
        return ''.join(random.choices(string.digits, k=length))

# For GET request, pre-generate random IDs
    user_id = generate_random_id()
    return render_template('signup.html', user_id=user_id)

# open acc
def generate_random_id(length=5):
    return ''.join(random.choices(string.digits, k=length))

def generate_random_acct_no(length=9):
    return ''.join(random.choices(string.digits, k=length))

# Open Digital Account Route
@app.route('/emp_dashboard/open_digital_account', methods=['GET', 'POST'])
def open_digital_account():
    if request.method == 'POST':
        # Retrieve form data
        customer_id = request.form.get('customer_id')
        branch_code = request.form.get('branchcode')
        acct_no = request.form.get('acctno')
        full_name = request.form.get('full_name')
        email = request.form.get('email')  
        phone_no = request.form.get('phone_no')
        address = request.form.get('address')
        d_o_b = request.form.get('d_o_b')
        marital_sts = request.form.get('marital_sts')
        nationality = request.form.get('nationality')
        gender = request.form.get('gender')
        id_card = request.form.get('id_card')
        source_of_income = request.form.get('soin')
        monthly_income = request.form.get('monthlyincom')  
        acct_type = request.form.get('acctyp')
        initial_deposit = request.form.get('init_dep_amo')
        account_purpose = request.form.get('acctporp')  
        card_req = request.form.get('cardreq')
        online_banking = request.form.get('online_banking')
        cheque_book = request.form.get('chequebook_req')
        sms_alert = request.form.get('sms_alert')
        checkbox = request.form.get('term_cond')

        # Print form data for debugging
        print("Received Data:", request.form)

        # Validate required fields
        if not all([customer_id, branch_code, acct_no, full_name, email, phone_no, address, d_o_b, marital_sts, 
                    nationality, gender, id_card, source_of_income, monthly_income, acct_type, initial_deposit, 
                    account_purpose, card_req, online_banking, cheque_book, sms_alert, checkbox]):
            error = "All fields are required!"
            return render_template('/emp_dashboard/open_digital_account.html', error=error)

        cursor = db.cursor()
        try:
            # Check if account already exists
            cursor.execute("SELECT * FROM open_digital_account WHERE Customer_ID = %s", (customer_id,))
            if cursor.fetchone():
                error = "Customer ID already exists!"
                return render_template('/emp_dashboard/open_digital_account.html', error=error)

            # Insert into database
            sql = """
                INSERT INTO open_digital_account (Customer_ID, Branch_Code, Account_Number, Full_Name, Email, Phone_Number, Address, 
                Date_of_Birth, Marital_Status, Nationality, Gender, ID_Card_Number, Source_of_Income, Monthly_Income, Account_Type, Initial_Deposit_Amount, 
                Account_Purpose, Debit_Card_Required, Online_Banking_Access, CheckBook_Request, SMS_Banking_Alerts, Term_and_Conditions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (customer_id, branch_code, acct_no, full_name, email, phone_no, address, d_o_b, marital_sts, 
                      nationality, gender, id_card, source_of_income, monthly_income, acct_type, initial_deposit, 
                      account_purpose, card_req, online_banking, cheque_book, sms_alert, checkbox)

            cursor.execute(sql, values)
            db.commit()
            
            return render_template('/emp_dashboard/open_digital_account.html', success=True)
        
        except MySQLdb.Error as e:
            error = f"Database error: {str(e)}"
            print(error)  # Log the error
            return render_template('/emp_dashboard/open_digital_account.html', error=error)

        finally:
            cursor.close()

    # Generate random IDs when the page is first loaded
    customer_id = generate_random_id()
    acct_no = generate_random_acct_no()
    return render_template('emp_dashboard/open_digital_account.html', customer_id=customer_id, acct_no=acct_no)

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

# loan application
@app.route('/loan_application')
def loan_application():
    def generate_random_id(length=5):
        return ''.join(random.choices(string.digits, k=length))
    
    # Generate the random IDs
    cust_id = generate_random_id()
    return render_template('admin_dashboard/loan_application.html', cust_id=cust_id)

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

# Run the app
if __name__ == '__main__':
    app.run(debug=True)