from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/budget_tracker"
mongo = PyMongo(app)


@app.route('/')
def index():
    return 'Welcome to Budget Tracker'


# Route for creating a new goal
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


# Route for getting all goals for a user
@app.route('/goals/<user_id>', methods=['GET'])
def get_goals(user_id):
    goals = mongo.db.goals.find({'user_id: user_id'})
    result = []
    for goal in goals:
        goal['_id'] = str(goal['_id'])
        result.append(goal)
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug=True)
