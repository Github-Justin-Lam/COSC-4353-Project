from flask import Flask, request, render_template

app = Flask(__name__)

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
    if len(city) > 100:
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
        return render_template('profile.html', error=error_statement)