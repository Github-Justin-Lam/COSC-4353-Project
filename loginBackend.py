from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField
from passlib.hash import sha256_crypt

app = Flask(__name__)

#configure db
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "password123"
app.config['MYSQL_DB'] = "flaskapp"

mysql = MySQL(app)

# Class for registration
class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    zip = IntegerField('Zip', [validators.Length(min=5, max=9)])
    address1 = StringField('Address1', [validators.Length(max=100)])
    address1 = StringField('Address2', [validators.Length(max=100)])
    city = StringField('City', [validators.Length(max=100)])
    state = StringField('State', [validators.Length(max=100)])
    confirm = PasswordField('Confirm Password')

@app.route('/')
def my_form():
    return render_template('login.html')

# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login.html'))
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)
    
    return render_template('login.html')

# User login
# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # Get Form Fields
#         username = request.form.get("username")
#         password = request.form.get("password")
#         # Check if this matches the "user" dictionary
#         print(username, User.get("username"))
#         print(password, User.get("password"))
#         if username == User.get("username") and password == User.get("password"):
#             error = 'Login Successful'
#             return render_template('login.html', error=error)
#         else:
#             error = 'User not found'
#             return render_template('login.html', error=error)
#     return render_template('login.html')