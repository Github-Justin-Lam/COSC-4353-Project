from flask import Flask, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

""" SQL CODE TO CREATE TABLE
CREATE TABLE fuelquote(
    gallons integer NOT NULL,
    delivery_date date NOT NULL,
    price float,
    total float
    );
"""

#configure db
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "password123"
app.config['MYSQL_DB'] = "flaskapp"

mysql = MySQL(app)

# Class for pricing module
class PricingModule:
    def __init__(self, gallons, delivery_address, delivery_date):
        price_per_gallon = gallons*3
        return price_per_gallon

@app.route('/')
def my_form():
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

@app.route('/', methods=['POST'])
def my_form_post():

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