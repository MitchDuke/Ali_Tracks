from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://DrMadKiller83:CodeInstitute83@myfirstcluster.3tmzjsu.mongodb.net/?retryWrites=true&w=majority&appName=myFirstCluster'
mongo = PyMongo(app)

@app.route('/update_total', methods=['POST'])
def update_total():
    month = request.json.get('month')

    # Increment total by £5 for the selected month
    mongo.db.aliTracks.update_one({}, {'$inc': {month: 5}})

    # Get updated total
    updated_total = mongo.db.aliTracks.find_one({})['total']

    return jsonify({'message': 'Total updated successfully', 'total': updated_total})


@app.route('/get_data')
def get_data():
    data = mongo.db.aliTracks.find()
    return jsonify(list(data))
