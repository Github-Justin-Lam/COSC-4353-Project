from flask import Flask, request, render_template

app = Flask(__name__)

# Class for pricing module
class PricingModule:
    def __init__(self, gallons, delivery_address, delivery_date):
        price_per_gallon = gallons*3
        return price_per_gallon

@app.route('/')
def my_form():
    return render_template('fuelquote.html')

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
        return render_template('fuelquote.html', error=error_statement)