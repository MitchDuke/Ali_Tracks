from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://DrMadKiller83:<password>@myfirstcluster.3tmzjsu.mongodb.net/?retryWrites=true&w=majority&appName=myFirstCluster'

mongo = PyMongo(app)

from flask import jsonify

@app.route('/get_data')
def get_data():
    data = mongo.db.aliTracks.find()
    return jsonify(list(data))
