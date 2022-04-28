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
    username varchar(25) PRIMARY KEY,
	fullname varchar(50) NOT NULL,
    address1 varchar(100) NOT NULL,
    address2 varchar(100),
    city varchar(100) NOT NULL,
    state char(2) NOT NULL,
    zipcode integer NOT NULL
		CONSTRAINT zipcode_length
        CHECK (zipcode between 10000 and 999999999));
CREATE TABLE fuelquote(
    username varchar(25) NOT NULL,
    FOREIGN KEY (username) REFERENCES profile(username),
    gallons integer NOT NULL,
    delivery_date date NOT NULL,
	address1 varchar(100) NOT NULL,
    address2 varchar(100),
    city varchar(100) NOT NULL,
    state char(2) NOT NULL,
    zipcode integer NOT NULL,
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
    cur = mysql.connection.cursor()
    #"IF NOT EXISTS (SELECT * FROM profile WHERE username = (user) VALUES (%s)",
    cur.execute("SELECT * FROM profile WHERE username = \"" + session['username'] + "\"") #select row from profile table
    #cur.execute("SELECT * FROM profile")
    profile = cur.fetchone() #fetches profile as a tuple
    print(profile)
    if not profile: #if profile not made yet, hide buttons
        return render_template('profile.html', error="Please fill your profile.", hide=True)
    else: #if profile made already, show current profile, enable navigation buttons
        name = profile[1]
        address1=profile[2] #corresponding index in tuple
        address2=profile[3]
        city=profile[4]
        state=profile[5]
        zipcode=profile[6]
        return render_template('profile.html', name=name, address1=address1,
            address2=address2, city=city, state=state, zip=zipcode, hide=False)

@app.route('/profile', methods=['POST'])
def profile_form_post():
    error_statement = ""
    errors = 0
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM profile WHERE username = \"" + session['username'] + "\"") #find if profile is made yet
    profile = cur.fetchone() #fetches profile as a tuple
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
        if not profile:
            return render_template('profile.html', error=error_statement,
                name=name, address1=address1, address2=address2, city=city, zip=zipcode, hide=True)
        else:
            return render_template('profile.html', error=error_statement,
                name=name, address1=address1, address2=address2, city=city, zip=zipcode, hide=False)
    else: #if no errors, add/change profile
        error_statement = "Profile Completed!"
        print(request.form)
        if not profile: #if profile not made yet, add profile, hide buttons
            cur.execute("INSERT INTO profile (username, fullname, address1, address2, city, state, zipcode) VALUES (%s,%s,%s,%s,%s,%s,%s)", (session['username'],name,address1,address2,city,state,zipcode))
            mysql.connection.commit()
            cur.close()
            return render_template('profile.html', error=error_statement, name=name, address1=address1, address2=address2, city=city, zip=zipcode, hide=False)
        else: #if profile made already, change profile, enable navigation
            cur.execute("UPDATE profile SET fullname=\""+name+"\", address1=\""+address1+"\", address2=\""+address2+"\", city=\""+city+"\", state=\""+state+"\", zipcode="+zipcode+" WHERE username=\""+session['username']+"\"")
            mysql.connection.commit()
            cur.close()
            return render_template('profile.html', error=error_statement, name=name, address1=address1, address2=address2, city=city, zip=zipcode, hide=False)

# Class for pricing module
class PricingModule:
    def __init__(self, username, gallons, state):
        #self.username = username
        #self.gallons = gallons
        #self.state = state
        if(state == "TX"):
            locationFactor = 0.02
            print("in-state")
        else:
            locationFactor = 0.04
            print("out-state")
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM fuelquote WHERE username = \"" + username + "\"") #select row from profile table
        fuelquote = cur.fetchone() #fetches one fuel quote as a tuple

        if(fuelquote == None):
            rateFactor = 0.00
            print("first time fuelquote")
        else: 
            rateFactor = 0.01
            print("returning user")
        
        if(int(gallons) >= 1000):
            gallonsFactor = 0.02
            print("gallons >= 1000")
        else:
            gallonsFactor = 0.03
            print("gallons < 1000")
        
        margin = (locationFactor - rateFactor + gallonsFactor + 0.1) * 1.50
        print("margin:", margin)
        self.suggestedPrice = 1.50 + margin
        print("self suggestedPrice:", self.suggestedPrice)
        self.total = int(gallons) * self.suggestedPrice
        print("self total:", self.total)

# Fuel Quote
@app.route('/fuelquote')
def fuelquote():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM profile WHERE username = \"" + session['username'] + "\"") #select row from profile table
    profile = cur.fetchone() #fetches profile as a tuple
    address1=profile[2] #corresponding index in tuple
    address2=profile[3]
    city=profile[4]
    state=profile[5]
    zipcode=profile[6]
    return render_template('fuelquote.html', address1=address1,
        address2=address2, city=city, state=state, zip=zipcode, hide=True)

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
    if request.method == 'POST':
        if request.form['submit'] == 'Calculate':
            if errors >= 1:
                return render_template('fuelquote.html', error=error_statement,
                    gallons=gallons, delivery_date=delivery_date, address1=address1, address2=address2, city=city, state=state, zip=zip)
            else: 
                error_statement = "Calculated Successfully!"
                print(request.form)

                calc = PricingModule(session['username'], gallons, state)
                print("price:", calc.suggestedPrice)
                print("total:", calc.total)

                return render_template('fuelquote.html', error=error_statement, gallons=gallons, delivery_date=delivery_date, address1=address1, address2=address2, city=city, state=state, zip=zip, price=calc.suggestedPrice, total=calc.total, hide=False)
        elif request.form['submit'] == 'Submit':
            error_statement = "Submitted Successfully!"

            price = request.form.get("price")
            print("price:", price)
            total = request.form.get("total")
            print("total:", total)

            #insert fuel quote into table
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO fuelquote (username, gallons, delivery_date, address1, address2, city, state, zipcode, price, total) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (session['username'], gallons, delivery_date, address1, address2, city, state, zip, price, total))
            mysql.connection.commit()
            cur.close()

            return render_template('fuelquote.html', error=error_statement, address1=address1, address2=address2, city=city, state=state, zip=zip)

# History
@app.route('/history')
def history():
    cur = mysql.connection.cursor()
    #cur.execute("SELECT * FROM profile WHERE username = \"" + session['username'] + "\"")
    #profile = cur.fetchone() #fetches profile as a tuple
    #address1=profile[2] #corresponding index in tuple
    #address2=profile[3]
    #city=profile[4]
    #state=profile[5]
    #zipcode=profile[6]
    #username = profile[0]

    cur.execute("SELECT * FROM fuelquote WHERE username = \"" + session['username'] + "\"")
    fuelquote = cur.fetchall() #fetches fuelquote as a tuple
    # for row in fuelquote:
        
    mysql.connection.commit()
    cur.close()

    return render_template('history.html', data = fuelquote)

if __name__ == "__main__":
    app.run(debug=True)