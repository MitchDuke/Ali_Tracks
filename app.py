import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_pymongo import PyMongo
from dotenv import load_dotenv

# Load environment variables from .env file
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

mongo = PyMongo(app)
print("MongoDB connected successfully!")

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/update_total', methods=['POST'])
def update_total():
    try:
        month = request.json.get('month')

        # Increment total by £5 for the selected month
        mongo.db.aliTracks.update_one({}, {'$inc': {'total': 5}})

        # Get updated total
        updated_total = mongo.db.aliTracks.find_one({})['total']

        return jsonify({'message': 'Total updated successfully', 'total': updated_total})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_total')
def get_total():
    try:
        data = mongo.db.aliTracks.find_one({})
        return jsonify({'total': data['total']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reset_total', methods=['POST'])
def reset_total():
    try:
        mongo.db.aliTracks.update_one({}, {'$set': {'total': 0}})
        return jsonify({'message': 'Total reset successfully', 'total': 0})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)
