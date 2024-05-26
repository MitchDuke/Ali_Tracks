import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo

app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = 'mongodb+srv://DrMadKiller83:CodeInstitute83@myfirstcluster.3tmzjsu.mongodb.net/'
mongo = PyMongo(app)
print("MongoDB connected successfully!")

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
