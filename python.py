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

# Homepage
@app.route('/')
def home():
    return render_template('first_screen.html')

# Account Management Page
@app.route('/emp_dashboard/account_manage_entity')
def account_manage_entity():
    return render_template('/emp_dashboard/account_manage_entity.html')

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

# balance
@app.route('/balance')
def balance():
    return render_template('/cust_dashboard/balance.html')

# report
@app.route('/reports')
def report():
    return render_template('/cust_dashboard/reports.html')

# customer dashboard
@app.route('/customer_dashboard')
def customer_dashboard():
    return render_template('/cust_dashboard/customer_dashboard.html')

#loan details
@app.route('/loan_detail')
def loan_detail():
    return render_template('/cust_dashboard/loan_detail.html')

# card mang
@app.route('/card_mang')
def card_mang():
    return render_template('/cust_dashboard/card_mang.html')

# Signup Page
def generate_random_id(length=5):
    """Generate a random numeric ID of specified length."""
    return ''.join(random.choices(string.digits, k=length))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data
        user_id = request.form.get('user_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')  
        phone_no = request.form.get('phone_no')
        address = request.form.get('address')
        d_o_b = request.form.get('d_o_b')
        gender = request.form.get('gender')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmpass')

        # Print form data for debugging
        print("Received Data:", request.form)

        # Validate required fields
        if not all([user_id, first_name, last_name, email, phone_no, address, 
                    d_o_b, gender, password, confirm_password]):
            error = "All fields are required!"
            return render_template('/signup.html', error=error)

        cursor = db.cursor()
        try:
            # Insert into database
            sql = """
                INSERT INTO signup (User_ID, First_Name, Last_Name, Email, Phone_No, Address, 
                Date_of_Birth, Gender, Password, Confirm_Password	)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (user_id, first_name, last_name, email, phone_no, address, 
                      d_o_b, gender, password, confirm_password)

            cursor.execute(sql, values)
            db.commit()
            
            return render_template('/signup.html', success=True)
        
        except MySQLdb.Error as e:
            error = f"Database error: {str(e)}"
            print(error)  # Log the error
            return render_template('/signup.html', error=error)

        finally:
            cursor.close()

# For GET request, pre-generate random IDs
    user_id = generate_random_id()
    return render_template('signup.html', user_id=user_id)

# Login Page
@app.route('/login_user_employee_auth', methods=['GET', 'POST'])
def login_user_employee_auth_page():
    if request.method == 'POST':
        # Get ID and password from the form
        userid = request.form.get('userid')
        password = request.form.get('password')

        print("Received Data:", request.form)

        # Check if both fields are filled
        if not all([userid, password]):
            error = "All fields are required!"
            return render_template('/login_user_employee_auth.html', error=error)

        cursor = db.cursor()
        try:
            # Check if user ID and password match in signup table
            cursor.execute("SELECT * FROM signup WHERE User_ID = %s AND Password = %s", (userid, password))
            user = cursor.fetchone()

            if user:
                # Log successful login
                cursor.execute("INSERT INTO login_authntication (ID, Password) VALUES (%s, %s)", (userid, password))
                db.commit()

                  # 3. Redirect to employee dashboard
                return render_template('/cust_dashboard/customer_dashboard.html')

                # Redirect based on ID and Password
            if userid == '1009828' and password == 'muhammadasad@2020':
                 return render_template('/emp_dashboard/account_manage_entity.html')
            elif userid == '1002319' and password == 'murtazaahmad@2020':
                return render_template('/admin_dashboard/manager_dashboard.html')
            else:
                error = "Invalid ID or Password!"
                return render_template('/login_user_employee_auth.html', error=error)

        except MySQLdb.Error as e:
            error = f"Database error: {str(e)}"
            print(error)
            return render_template('/login_user_employee_auth.html', error=error)

        finally:
            cursor.close()

    # GET request shows login form
    return render_template('/login_user_employee_auth.html')

# Route to Get Total Balance from Deposit Table
@app.route('/get_balance', methods=['GET'])
def get_balance():
    cursor = db.cursor()
    cursor.execute("SELECT SUM(amount) AS total_balance FROM deposit")  # Adjust table name if needed
    result = cursor.fetchone()
    total_balance = result['total_balance'] if result['total_balance'] else 0  # Handle NULL case
    return jsonify({'balance': total_balance})

# open acc
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
    acct_no = generate_random_acct_no()
    return render_template('emp_dashboard/open_digital_account.html', acct_no=acct_no)

# card management
def generate_random_card_no(length=16):
    return ''.join(random.choices(string.digits, k=length))

def generate_random_cvv(length=3):
    return ''.join(random.choices(string.digits, k=length))
    
# card management
@app.route('/emp_dashboard/card_management', methods=['GET', 'POST'])
def card_management():
    if request.method == 'POST':
        # Retrieve form data
        custm_id = request.form.get('custm_id')
        card_type = request.form.get('card_typ')
        card_no = request.form.get('card_no')
        holder_name = request.form.get('holder_name')
        issue_date = request.form.get('issue_date')
        expiry_date = request.form.get('expiry_date')
        cvv = request.form.get('cvv')
        id_card = request.form.get('id_card')
        international_trns = request.form.get('international_trns')
        daily_limit = request.form.get('daily_limit')
        term_cond = request.form.get('term_cond')

        # Print form data for debugging
        print("Received Data:", request.form)

        # Validate required fields
        if not all([custm_id, card_type, card_no, holder_name, issue_date, 
                    expiry_date, cvv, id_card, international_trns, daily_limit, term_cond]):
            error = "All fields are required!"
            return render_template('/emp_dashboard/card_management.html', error=error)

        cursor = db.cursor()
        try:
            # Check if card already exists
            cursor.execute("SELECT * FROM apply_card WHERE Customer_ID = %s", (custm_id,))
            if cursor.fetchone():
                error = "Customer ID already exists!"
                return render_template('/emp_dashboard/card_management.html', error=error)

            # Insert into database
            sql = """
                INSERT INTO apply_card (Customer_ID, Card_Type, Card_Number, Card_Holder_Name, 
                Card_Issue_Date, Card_Expiry_Date, CVV, ID_Card_Number, Allow_International_Transaction, 
                Daliy_Withdrawal_Limit, Term_and_Conditions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (custm_id, card_type, card_no, holder_name, issue_date, expiry_date, 
                      cvv, id_card, international_trns, daily_limit, term_cond)

            cursor.execute(sql, values)
            db.commit()
            
            return render_template('/emp_dashboard/card_management.html', success=True)
        
        except MySQLdb.Error as e:
            error = f"Database error: {str(e)}"
            print(error)  # Log the error
            return render_template('/emp_dashboard/card_management.html', error=error)

        finally:
            cursor.close()
            
    # Generate the random IDs
    card_no = generate_random_card_no()
    cvv = generate_random_cvv()
    return render_template('emp_dashboard/card_management.html', card_no=card_no, cvv=cvv)

# blocked acc
@app.route('/emp_dashboard/blocked_acc' , methods=['GET', 'POST'])
def blocked_accounts():
    if request.method == 'POST':
        # Retrieve form data
        custm_id = request.form.get('customer_id')
        branchcode = request.form.get('branchcode')
        acctno = request.form.get('acctno')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone_no = request.form.get('phone_no')
        id_card = request.form.get('id_card')
        acctyp = request.form.get('acctyp')
        acctporp = request.form.get('acctporp')
        term_cond = request.form.get('term_cond')

        # Print form data for debugging
        print("Received Data:", request.form)

        # Validate required fields
        if not all([custm_id, branchcode, acctno, full_name, email, phone_no, 
                    id_card, acctyp, acctporp, term_cond]):
            error = "All fields are required!"
            return render_template('/emp_dashboard/blocked_acc.html', error=error)
        
        cursor = db.cursor()
        try:
            # Check if card already exists
            cursor.execute("SELECT * FROM blocked_acc WHERE Customer_ID = %s", (custm_id,))
            if cursor.fetchone():
                error = "Customer ID already exists!"
                return render_template('/emp_dashboard/blocked_acc.html', error=error)
            
             # Insert into database
            sql = """
                INSERT INTO blocked_acc (Customer_ID, Branch_Code, Account_Number, Full_Name, Email, Phone_No, 
                ID_Card_Number, Account_Type, Account_Purpose, Term_and_Conditions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (custm_id, branchcode, acctno, full_name, email, phone_no, 
                      id_card, acctyp, acctporp, term_cond)

            cursor.execute(sql, values)
            db.commit()
            
            return render_template('/emp_dashboard/blocked_acc.html', success=True)
        
        except MySQLdb.Error as e:
            error = f"Database error: {str(e)}"
            print(error)  # Log the error
            return render_template('/emp_dashboard/blocked_acc.html', error=error)

        finally:
            cursor.close()

    return render_template('/emp_dashboard/blocked_acc.html')

# cheque book management
@app.route('/emp_dashboard/chequebook_management', methods=['GET', 'POST'])
def cheque_book_management():
    if request.method == 'POST':
        # Retrieve form data
        custm_id = request.form.get('customer_id')
        holder_name = request.form.get('holder_name')
        acctno = request.form.get('account_no')
        acctyp = request.form.get('acctyp')
        branch_name = request.form.get('branch_name')
        book_pages = request.form.get('book_pages')
        chequebook_typ = request.form.get('chequebook_typ')
        delivery_mode = request.form.get('delivery_mode')
        process_time = request.form.get('process_time')
        term_cond = request.form.get('term_cond')

        # Print form data for debugging
        print("Received Data:", request.form)

        # Validate required fields
        if not all([custm_id, holder_name, acctno,  acctyp, branch_name, book_pages, chequebook_typ, delivery_mode, process_time, term_cond]):
            error = "All fields are required!"
            return render_template('/emp_dashboard/chequebook_management.html', error=error)
        
        cursor = db.cursor()
        try:
            # Check if card already exists
            cursor.execute("SELECT * FROM chequebook_management WHERE Customer_ID = %s", (custm_id,))
            if cursor.fetchone():
                error = "Customer ID already exists!"
                return render_template('/emp_dashboard/chequebook_management.html', error=error)
            
             # Insert into database
            sql = """
                INSERT INTO chequebook_management (Customer_ID, Account_Holder_Name, Account_Number, Account_Type, Branch_Name, ChequeBook_Leaves, 
                ChequeBook_Type, ChequeBook_Delivery_Mode, Urgent_Processing_Required, Term_and_Conditions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = ([custm_id, holder_name, acctno,  acctyp, branch_name, book_pages, chequebook_typ, delivery_mode, process_time, term_cond])

            cursor.execute(sql, values)
            db.commit()
            
            return render_template('/emp_dashboard/chequebook_management.html', success=True)
        
        except MySQLdb.Error as e:
            error = f"Database error: {str(e)}"
            print(error)
            return render_template('/emp_dashboard/chequebook_management.html', error=error)
        finally:
            cursor.close()

    return render_template('.html')

# deposit money
@app.route('/emp_dashboard/deposit_money', methods=['GET', 'POST'])
def depositmoney():
    if request.method == 'POST':
        # Retrieve form data
        customer_id = request.form.get('cus_id')
        currency = request.form.get('currency')
        branch_code = request.form.get('branchcode')
        acc_holder_name = request.form.get('acc_holder_name')
        account_number = request.form.get('acc_num')
        tody_date = request.form.get('tody_date')
        denom = request.form.get('denom')
        count = request.form.get('count')
        total = request.form.get('total')
        deposit_by = request.form.get('deposit_by')
        receiver_by = request.form.get('receiver_by')
        id_card = request.form.get('id_card')
        phn_no = request.form.get('phn_no')
        term_cond = request.form.get('term_cond')

        # Print form data for debugging
        print("Received Data:", request.form)

        # Validate required fields
        if not all([customer_id, currency, branch_code, acc_holder_name, account_number, tody_date, denom, 
                    count, total, deposit_by, receiver_by, id_card, phn_no, term_cond]):
            error = "All fields are required!"
            return render_template('/emp_dashboard/deposit_money.html', error=error)
        
        cursor = db.cursor()
        try:
            # Check if card already exists
            cursor.execute("SELECT * FROM deposite_money WHERE Customer_ID = %s", (customer_id,))
            if cursor.fetchone():
                error = "Customer ID already exists!"
                return render_template('/emp_dashboard/deposit_money.html', error=error)
            
             # Insert into database
            sql = """
                INSERT INTO deposite_money (Customer_ID, Currency, Branch_Code, Account_Holder_Name, Account_Number, Date, Denominations, 
                Number_of_Notes, Total_Amount, Depositer_Name, Receiver_Name, ID_Card_Number, Contact_Number, Term_and_Conditions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = ([customer_id, currency, branch_code, acc_holder_name, account_number, tody_date, denom, 
                    count, total, deposit_by, receiver_by, id_card, phn_no, term_cond])

            cursor.execute(sql, values)
            db.commit()
            
            return render_template('/emp_dashboard/deposit_money.html', success=True)
        
        except MySQLdb.Error as e:
            error = f"Database error: {str(e)}"
            print(error)
            return render_template('/emp_dashboard/deposit_money.html', error=error)
        finally:
            cursor.close()

    return render_template('/emp_dashboard/deposit_money.html')

# add user
@app.route('/add_user')
def add_user():
    def generate_random_id(length=5):
        return ''.join(random.choices(string.digits, k=length))
    
    # Generate the random IDs
    user_id = generate_random_id()

    return render_template('admin_dashboard/add_user.html', user_id=user_id)

@app.route('/admin_dashboard/add_user', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        # Retrieve form data
        user_id = request.form.get('user_id')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_no = request.form.get('phone_no')
        d_o_b = request.form.get('d_o_b')
        designation = request.form.get('designation')
        Salary = request.form.get('salary')
        d_o_join = request.form.get('d_o_join')
        term_cond = request.form.get('term_cond')

         # Print form data for debugging
        print("Received Data:", request.form)

        # Validate required fields
        if not all([user_id, first_name, last_name, email, phone_no, d_o_b, designation, Salary, d_o_join, term_cond]):
            error = "All fields are required!"
            return render_template('/admin_dashboard/add_user.html', error=error)
        
        cursor = db.cursor()
        try:
            # Check if card already exists
            cursor.execute("SELECT * FROM add_user WHERE Employee_ID = %s", (user_id,))
            if cursor.fetchone():
                error = "Employee ID already exists!"
                return render_template('/admin_dashboard/add_user.html', error=error)
            
             # Insert into database
            sql = """
                INSERT INTO add_user (Employee_ID, First_Name, Last_Name, Email, Phone_Number, Date_of_Birth, 
                User_Designation, Salary_Per_Month, Date_of_Joining, Term_and_Conditions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = ([user_id, first_name, last_name, email, phone_no, d_o_b, designation, Salary, d_o_join, term_cond])

            cursor.execute(sql, values)
            db.commit()
            
            return render_template('/admin_dashboard/add_user.html', success=True)
        
        except MySQLdb.Error as e:
            error = f"Database error: {str(e)}"
            print(error)
            return render_template('/admin_dashboard/add_user.html', error=error)

        finally:
            cursor.close()

    return render_template('/admin_dashboard/add_user.html')

# loan application
@app.route('/admin_dashboard/loan_application', methods=['GET', 'POST'])
def loan_app():
    if request.method == 'POST':
        #Retrieve form data
        customer_id = request.form.get('cust_id')
        acctno = request.form.get('acctno')
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        phone_no = request.form.get('phone_no')
        id_card = request.form.get('id_card')
        loan_typ = request.form.get('loan_typ')
        amont_req = request.form.get('amont_req')
        application_date = request.form.get('application_date')
        return_date = request.form.get('return_date')
        loan_period = request.form.get('loan_period')
        application_stats = request.form.get('application_stats')
        term_cond = request.form.get('term_cond')

        # Print form data for debugging
        print("Received Data:", request.form)

        # Validate required fields
        if not all([customer_id, acctno, full_name, email, phone_no, id_card, loan_typ, amont_req, 
                    application_date, return_date, loan_period, application_stats, term_cond]):
            error = "All fields are required!"
            return render_template('/admin_dashboard/loan_application.html', error=error)
        
        cursor = db.cursor()
        try:
            # Check if card already exists
            cursor.execute("SELECT * FROM loan_application WHERE Customer_ID = %s", (customer_id,))
            if cursor.fetchone():
                error = "Customer ID already exists!"
                return render_template('/admin_dashboard/loan_application.html', error=error)
            
             # Insert into database
            sql = """
                INSERT INTO loan_application (Customer_ID, Account_Number, Full_Name, Email, Phone_Number, ID_Card_Number, 
                Loan_Type, Amount_Requested, Application_Date, Return_Date, Loan_Period, Application_Status, Term_and_Conditions)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s)
            """
            values = ([customer_id, acctno, full_name, email, phone_no, id_card, loan_typ, amont_req, 
                       application_date, return_date, loan_period, application_stats, term_cond])

            cursor.execute(sql, values)
            db.commit()
            
            return render_template('/admin_dashboard/loan_application.html', success=True)
        
        except MySQLdb.Error as e:
            error = f"Database error: {str(e)}"
            print(error)
            return render_template('/admin_dashboard/loan_application.html', error=error)
        
        finally:
            cursor.close()

    return render_template('/admin_dashboard/loan_application.html')

# report
@app.route('/cust_dashboard/reports', methods=['GET', 'POST'])
def reports():
    if request.method == 'POST':
        # Retrieve form data
        c_id = request.form.get('c_id')
        c_name = request.form.get('c_name')
        remarks = request.form.get('remarks')

        # Print form data for debugging
        print("Received Data:", request.form)

        # Validate required fields
        if not all([c_id, c_name, remarks]):
            error = "All fields are required!"
            return render_template('/cust_dashboard/reports.html', error=error)
        
        cursor = db.cursor()
        try:
            # Insert into database
            sql = """
                INSERT INTO report (Customer_ID, Customer_Name, Report_and_FeedBack)
                VALUES (%s, %s, %s)
            """
            values = ([c_id, c_name, remarks])

            cursor.execute(sql, values)
            db.commit()
            
            return render_template('/cust_dashboard/reports.html', success=True)
        
        except MySQLdb.Error as e:
            error = f"Database error: {str(e)}"
            print(error)
            return render_template('/cust_dashboard/reports.html', error=error)

        finally:
            cursor.close()

    return render_template('/cust_dashboard/reports.html')

# Get Customer Balance  
@app.route('/get_customer_balance', methods=['GET', 'POST'])
def get_customer_balance():
    customer_id = request.args.get('customer_id')
    
    cursor = db.cursor()
    try:
        cursor.execute("SELECT SUM(Total_Amount) FROM deposite_money WHERE Customer_ID = %s", (customer_id,))
        result = cursor.fetchone()
        total_balance = result[0] if result[0] is not None else 0
        return jsonify({'balance': total_balance})
    except Exception as e:
        print("Error fetching customer balance:", e)
        return jsonify({'balance': 0})

#Get Customer Loan Details
@app.route('/cust_dashboard/loan_detail', methods=['GET', 'POST'])
def get_customer_loan_details():
    id_card = request.form.get('id_card')  # Because you're using POST and form
    
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM loan_application WHERE ID_Card_Number = %s", (id_card,))
        result = cursor.fetchall()

        # Convert DB results into dictionaries for Jinja2 template
        columns = [desc[0] for desc in cursor.description]
        loan_list = [dict(zip(columns, row)) for row in result]

        return render_template('/cust_dashboard/loan_detail.html', loan_list=loan_list)
    except Exception as e:
        print("Error fetching customer loan details:", e)
        return render_template('/cust_dashboard/loan_detail.html', loan_list=[], error="Error fetching data")
    
# Run the app
if __name__ == '__main__':
    app.run(debug=True)