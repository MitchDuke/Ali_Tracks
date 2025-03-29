import os
from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
from bson.objectid import ObjectId

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
goals_collection = mongo.db.goals

if mongo.db is None:
    raise ValueError("Failed to connect to MongoDB. Check your MONGO_URI and database configuration.")


# register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Route for the registration page."""
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users_collection.insert_one(
            {'username': user, 'password': hashed_password})
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')


# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    """Route for the login page."""
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


# Logout route
@app.route('/logout')
def logout():
    """Route to logout."""
    session.pop('username', None)
    flash('You have been logged out!')
    return redirect(url_for('login'))


# Index route
@app.route('/index')
def index():
    """Route to the savings page /index page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


# Update total route
@app.route('/update_total', methods=['POST'])
def update_total():
    """Update the total in the database."""
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        month = request.json.get('month')
        username = session['username']
        print(f"Received request to update total for month: {month}")

        # Ensure there is a document in the collection
        if not savings_collection.find_one({'username': username}):
            savings_collection.insert_one(
                {'username': username, 'total': 0})

        savings_collection.update_one({'username': username}, {
                                      '$inc': {'total': 5}})
        updated_total = savings_collection.find_one(
            {'username': username})['total']
        print(f"Updated total for {username}: {updated_total}")

        # Return the updated total
        return jsonify({'message': 'Total updated successfully', 'total': updated_total})
    except Exception as e:
        print(f"Error updating total: {e}")
        return jsonify({'error': str(e)}), 500


# Get total route
@app.route('/get_total')
def get_total():
    """Get total from the database."""
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        username = session['username']
        data = savings_collection.find_one({'username': username})
        if data is None:
            data = {'total': 0}
            savings_collection.insert_one(
                {'username': username, 'total': 0})
        print(f"Current total for {username}: {data['total']}")
        return jsonify({'total': data['total']})
    except Exception as e:
        print(f"Error fetching total: {e}")
        return jsonify({'error': str(e)}), 500


# Reset total route
@app.route('/reset_total', methods=['POST'])
def reset_total():
    """Reset the total to 0."""
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        username = session['username']
        savings_collection.update_one(
            {'username': username}, {'$set': {'total': 0}})
        print(f"Total reset to 0 for {username}")
        return jsonify({'message': 'Total reset successfully', 'total': 0})
    except Exception as e:
        print(f"Error resetting total: {e}")
        return jsonify({'error': str(e)}), 500


# Contact page route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Route for the contact page."""
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        contact_collection.insert_one(
            {'name': name, 'message': message})  # Insert message in database
        flash('Message sent successfully, thank you!')
        return redirect(url_for('index'))
    return render_template('contact.html')


# Goals page route
@app.route('/goals')
def goals():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    user_goals = list(goals_collection.find({'username': username}))
    return render_template('goals.html', goals=user_goals)


# Create goal route
@app.route('/create-goal', methods=['POST'])
def create_goal():
    if 'username' not in session:
        return redirect(url_for('login'))

    goal_name = request.form['goal_name']
    target_amount = int(request.form['target_amount'])
    username = session['username']

    goal = {
        'username': session['username'],
        'goal_name': goal_name,
        'target_amount': target_amount,
        'current_amount': 0,
        'status': 'in-progress'
    }

    goals_collection.insert_one(goal)
    flash('Goal created successfully!')
    return redirect(url_for('goals'))


# Update goal route
@app.route('/update-goal', methods=['POST'])
def update_goal():
    if 'username' not in session:
        return redirect(url_for('login'))

    goal_id = request.form['goal_id']
    amount = int(request.form['amount'])

    goals_collection.update_one(
        {'_id': ObjectId(goal_id)},
        {'$inc': {'current_amount': amount}}
    )
    flash('Goal updated successfully!')
    return redirect(url_for('goals'))


# Delete goal route
@app.route('/delete-goal', methods=['POST'])
def delete_goal():
    if 'username' not in session:
        return redirect(url_for('login'))

    goal_id = request.form['goal_id']

    goals_collection.delete_one({'_id': ObjectId(goal_id)})
    flash('Goal deleted successfully!')
    return redirect(url_for('goals'))


if __name__ == '__main__':
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=False
    )
