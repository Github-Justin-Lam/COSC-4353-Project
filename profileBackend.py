from flask import Flask, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

""" SQL CODE TO CREATE TABLE/DATABASE
CREATE DATABASE flaskapp;
USE flaskapp;
CREATE TABLE profile(
	fullname varchar(50) NOT NULL,
    address1 varchar(100) NOT NULL,
    address2 varchar(100),
    city varchar(100) NOT NULL,
    state char(2) NOT NULL,
    zipcode integer NOT NULL
		CONSTRAINT zipcode_length
        CHECK (zipcode between 10000 and 999999999));
"""
#configure db
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "password123"
app.config['MYSQL_DB'] = "flaskapp"

mysql = MySQL(app)

@app.route('/')
def my_form():
    return render_template('profile.html')

@app.route('/', methods=['POST'])
def my_form_post():
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