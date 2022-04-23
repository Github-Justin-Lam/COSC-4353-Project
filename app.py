from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = "super secret key"

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "password123"
app.config['MYSQL_DB'] = "flaskapp"

mysql = MySQL(app)

""" SQL CODE TO CREATE TABLE/DATABASE
CREATE DATABASE flaskapp;
USE flaskapp;
CREATE TABLE users(
	username varchar(25) PRIMARY KEY,
    password varchar(100) NOT NULL);
CREATE TABLE profile(
	fullname varchar(50) NOT NULL,
    address1 varchar(100) NOT NULL,
    address2 varchar(100),
    city varchar(100) NOT NULL,
    state char(2) NOT NULL,
    zipcode integer NOT NULL
		CONSTRAINT zipcode_length
        CHECK (zipcode between 10000 and 999999999));
CREATE TABLE fuelquote(
    gallons integer NOT NULL,
    delivery_date date NOT NULL,
    price float,
    total float);
"""

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
    if request.method == 'POST':
        username = request.form.get("username")
        password = sha256_crypt.encrypt(str(request.form.get("password")))
        print(username, password)
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')
        error = 'You are now registered and can log in'
        #return redirect(url_for('login'))
        return render_template('login.html', error=error)
    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        # Get Form Fields
        username = request.args.get("username")
        print(username)
        password_candidate = request.args.get("password")
        
        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        sqlinput = "SELECT * FROM users WHERE username = " + "\"" + str(username) + "\""
        result = cur.execute(sqlinput)
        print(result)
        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            print(data)
            password = data[1]

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                #return redirect(url_for('dashboard'))
                #error = 'You are now logged in'
                #return render_template('login.html', error=error)
                return redirect("/profile")
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Profile
@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/profile', methods=['POST'])
def profile_form_post():
    error_statement = ""
    errors = 0
    name = request.form.get("name")
    if len(name) > 50 or len(name) <= 0:
        error_statement += "\nA name is required & can only be up to 50 characters"
        errors += 1
    address1 = request.form.get("address1")
    if len(address1) > 100 or len(address1) <= 0:
        error_statement += "\nAn address is required & can only be up to 100 characters"
        errors += 1
    address2 = request.form.get("address2")
    if len(address2) > 100:
        error_statement += "\nAn address can only be up to 100 characters"
        errors += 1
    city = request.form.get("city")
    if len(city) > 100 or len(city) <= 0:
        error_statement += "\nA city is required & can only be up to 100 characters"
        errors += 1
    state = request.form.get("state")
    if state == "":
        error_statement += "\nA state is required"
        errors += 1
    zipcode = request.form.get("zip")
    if len(zipcode) > 9 or len(zipcode) < 5:
        error_statement += "\nA zipcode is required & must be between 5-9 characters"
        errors += 1
    print(errors, "errors encountered.", error_statement)
    if errors >= 1:
        return render_template('profile.html', error=error_statement,
            name=name, address1=address1, address2=address2, city=city, zip=zipcode)
    else: 
        error_statement = "Profile Completed!"
        print(request.form)
        #if no errors, insert profile info to table
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO profile (fullname, address1, address2, city, state, zipcode) VALUES (%s,%s,%s,%s,%s,%s)", (name,address1,address2,city,state,zipcode))
        mysql.connection.commit()
        cur.close()
        return render_template('profile.html', error=error_statement)

# Class for pricing module
class PricingModule:
    def __init__(self, gallons, delivery_address, delivery_date):
        price_per_gallon = gallons*3
        return price_per_gallon
# Fuel Quote
@app.route('/fuelquote')
def fuelquote():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM profile") #select row from profile table
    profile = cur.fetchone() #fetches profile as a tuple
    address1=profile[1] #corresponding index in tuple
    address2=profile[2]
    city=profile[3]
    state=profile[4]
    zipcode=profile[5]
    return render_template('fuelquote.html', address1=address1,
        address2=address2, city=city, state=state, zip=zipcode)

@app.route('/fuelquote', methods=['POST'])
def fuelquote_post():

    error_statement = ""
    errors= 0

    gallons = request.form.get("gallons")
    if int(gallons) <= 0:
        error_statement += "\nGallons must be greater than 0."
        errors += 1
    print("gallons:", gallons)

    address1 = request.form.get("address1")
    print("address1:", address1)

    address2 = request.form.get("address2")
    print("address2:", address2)

    city = request.form.get("city")
    print("city:", city)

    state = request.form.get("state")
    print("state:", state)

    zip = request.form.get("zip")
    print("zip:", zip)

    delivery_date = request.form.get("delivery_date")
    print("delivery_date:", delivery_date)

    print(errors, "errors encountered.", error_statement)
    if errors >= 1:
        return render_template('fuelquote.html', error=error_statement,
            gallons=gallons, delivery_date=delivery_date)
    else: 
        error_statement = "Fuel Quote Submitted!"
        print(request.form)
        #if no errors, insert fuelquote info to table
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO fuelquote (gallons, delivery_date) VALUES (%s,%s)", (gallons, delivery_date))
        mysql.connection.commit()
        cur.close()
        return render_template('fuelquote.html', error=error_statement)

# History
@app.route('/history')
def history():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM profile")
    profile = cur.fetchone() #fetches profile as a tuple
    address1=profile[1] #corresponding index in tuple
    address2=profile[2]
    city=profile[3]
    state=profile[4]
    zipcode=profile[5]

    cur.execute("SELECT * FROM fuelquote")
    fuelquote = cur.fetchall() #fetches fuelquote as a tuple
    mysql.connection.commit()
    cur.close()

    return render_template('history.html', address1=address1,
        address2=address2, city=city, state=state, zip=zipcode, data = fuelquote)

if __name__ == "__main__":
    app.run(debug=True)