from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# Load environment variables from .env file
if os.path.exists(".env"):
    load_dotenv()

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)

# Get the MONGO_URI and SECRET_KEY from environment variables
mongo_uri = os.environ.get('MONGO_URI')
secret_key = os.environ.get('SECRET_KEY')
print("MongoDB connected successfully!")

# Check if the environment variables are loaded correctly
if not mongo_uri:
    raise ValueError("MONGO_URI environment variable is not set.")
if not secret_key:
    raise ValueError("SECRET_KEY environment variable is not set.")

app.config['MONGO_URI'] = mongo_uri
app.config['SECRET_KEY'] = secret_key

# Initialize PyMongo with the Flask app
mongo = PyMongo(app)
users_collection = mongo.db.users
savings_collection = mongo.db.savings
contact_collection = mongo.db.contacts

if mongo.db is None:
    raise ValueError("Failed to connect to MongoDB. Check your MONGO_URI "
                     "and database configuration.")

# Route for the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users_collection.insert_one({'username': user, 'password': hashed_password})
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})
        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials, please try again!')
    return render_template('login.html')

# Route to logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out!')
    return redirect(url_for('login'))

# Route to the savings page /index page
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

# Update the total in the database
@app.route('/update_total', methods=['POST'])
def update_total():
    if 'username' not in session:  # Fixed condition here
        return redirect(url_for('login'))

    try:
        month = request.json.get('month')
        username = session['username']
        print(f"Received request to update total for month: {month}")

        # Ensure there is a document in the collection
        if not savings_collection.find_one({'username': username}):
            savings_collection.insert_one({'username': username, 'total': 0})

        savings_collection.update_one({'username': username}, {'$inc': {'total': 5}})
        updated_total = savings_collection.find_one({'username': username})['total']
        print(f"Updated total for {username}: {updated_total}")

        # Return the updated total
        return jsonify({'message': 'Total updated successfully', 'total': updated_total})
    except Exception as e:
        print(f"Error updating total: {e}")
        return jsonify({'error': str(e)}), 500

# Get total from the database
@app.route('/get_total')
def get_total():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        username = session['username']
        data = savings_collection.find_one({'username': username})
        if data is None:
            data = {'total': 0}
            savings_collection.insert_one({'username': username, 'total': 0})
        print(f"Current total for {username}: {data['total']}")
        return jsonify({'total': data['total']})
    except Exception as e:
        print(f"Error fetching total: {e}")
        return jsonify({'error': str(e)}), 500

# Reset the total to 0
@app.route('/reset_total', methods=['POST'])
def reset_total():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        username = session['username']
        savings_collection.update_one({'username': username}, {'$set': {'total': 0}})
        print(f"Total reset to 0 for {username}")
        return jsonify({'message': 'Total reset successfully', 'total': 0})
    except Exception as e:
        print(f"Error resetting total: {e}")
        return jsonify({'error': str(e)}), 500

# Route for the contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        contact_collection.insert_one({'name': name, 'message': message})  # Insert message into the database
        # Send the message to the database
        flash('Message sent successfully, thank you!')
        return redirect(url_for('index'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
