from flask import Flask, render_template, request, redirect, url_for, session
from blood_bank_management import *
app = Flask(__name__)
app.secret_key = 'key_here'
blood_bank = BloodBankManagement()
# Mock user database (replace with your authentication logic)
users = {'admin': 'password'}

# Define routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/add_donor', methods=['GET', 'POST'])
def add_donor():
    if request.method == 'POST':
        # Process the form data submitted by the user
        name = request.form['name']
        blood_type = request.form['blood_type']
        phone_number = request.form['phone_number']
        city = request.form['city']
        state = request.form['state']
        blood_bank.add_donor(name, blood_type, phone_number, city, state)
        return redirect(url_for('home'))  # Redirect to the home page after processing the form data
    else:
        return render_template('add_donor.html')

@app.route('/add_recipient', methods=['GET', 'POST'])
def add_recipient():
    if request.method == 'POST':
        name = request.form['name']
        blood_type = request.form['blood_type']
        phone_number = request.form['phone_number']
        city = request.form['city']
        state = request.form['state']
        blood_bank.add_recipient(name, blood_type, phone_number, city, state)
        return redirect(url_for('home'))
    return render_template('add_recipient.html')

@app.route('/search_donors', methods=['GET', 'POST'])
def search_donors():
    if request.method == 'POST':
        blood_type = request.form['blood_type']
        city = request.form.get('city')
        state = request.form.get('state')
        donors = blood_bank.search_donors(blood_type, city, state)
        return render_template('search_donors.html', donors=donors)
    return render_template('search_donors.html')

@app.route('/search_recipients', methods=['GET', 'POST'])
def search_recipients():
    if request.method == 'POST':
        blood_type = request.form['blood_type']
        city = request.form.get('city')
        state = request.form.get('state')
        recipients = blood_bank.search_recipients(blood_type, city, state)
        return render_template('search_recipients.html', recipients=recipients)
    return render_template('search_recipients.html')

if __name__ == '__main__':
    app.run(debug=True)
