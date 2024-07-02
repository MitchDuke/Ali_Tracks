from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
from flash_bcyrpt import Bcrypt
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# Load environment variables from .env file
if os.path.exists(".env"):
    load_dotenv()

app = Flask(__name__)
CORS(app)

# Get the MONGO_URI and SECRET_KEY from environment variables
mongo_uri = os.environ.get('MONGO_URI')
secret_key = os.environ.get('SECRET_KEY')

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

if mongo.db is None:
    raise ValueError("Failed to connect to MongoDB. Check your MONGO_URI "
                     "and database configuration.")

print("MongoDB connected successfully!")

# Reference the correct collection
monthly_tracker = mongo.db.monthlyTracker


# Define the routes for the html page
@app.route("/")


def index():
    return render_template("index.html")


@app.route('/update_total', methods=['POST'])


# Update the total in the database
def update_total():
    try:
        month = request.json.get('month')
        print(f"Received request to update total for month: {month}")

        # Ensure there is a document in the collection
        if not monthly_tracker.find_one({}):
            monthly_tracker.insert_one({'total': 0})

        # Increment total by £5 for the selected month
        monthly_tracker.update_one({}, {'$inc': {'total': 5}})

        # Get updated total
        updated_total = monthly_tracker.find_one({})['total']
        print(f"Updated total: {updated_total}")

        # Return the updated total
        return jsonify({'message': 'Total updated successfully',
                        'total': updated_total})
    except Exception as e:
        print(f"Error updating total: {e}")
        return jsonify({'error': str(e)}), 500

# Get total from the database
@app.route('/get_total')


def get_total():
    try:
        data = monthly_tracker.find_one({})
        if data is None:
            data = {'total': 0}
            monthly_tracker.insert_one(data)
        print(f"Current total: {data['total']}")
        return jsonify({'total': data['total']})
    except Exception as e:
        print(f"Error fetching total: {e}")
        return jsonify({'error': str(e)}), 500

# Reset the total to 0
@app.route('/reset_total', methods=['POST'])


def reset_total():
    try:
        monthly_tracker.update_one({}, {'$set': {'total': 0}})
        print("Total reset to 0")
        return jsonify({'message': 'Total reset successfully', 'total': 0})
    except Exception as e:
        print(f"Error resetting total: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=False)
