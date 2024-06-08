import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_pymongo import PyMongo

if os.path.exists("env.py"):
    import env

app = Flask(__name__)
CORS(app)

app.config['MONGO_URI'] = os.eviron.get('mongodb+srv://DrMadKiller83:CodeInstitute83@myfirstcluster.3tmzjsu.mongodb.net/')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
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
