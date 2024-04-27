from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/budget_tracker"
mongo = PyMongo(app)

@app.route('/goal', methods=['POST'])
def create_goal():
    data = request.json
    title =data.get('title')
    target_amount = data.get('target_amount')
    current_amount = data.get('current_amount', 0)
    user_id = data.get('user_id')


    goal = {
        'title': title,
        'target_amount': target_amount,
        'current_amount': current_amount,
        'user_id': user_id
    }


    mongo.db.goals.insert_one(goal)
    return jsonify({'message': 'Goal created successfully'}), 201


@app.route('/')
def index():
    return 'Welcome to Budget Tracker'

if __name__ == '__main__':
    app.run(debug=True)
