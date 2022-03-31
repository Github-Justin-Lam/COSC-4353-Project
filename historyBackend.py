from flask import Flask, request, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

#configure db
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "password123"
app.config['MYSQL_DB'] = "flaskapp"

mysql = MySQL(app)

@app.route('/')
def my_form():
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