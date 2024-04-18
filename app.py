from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/budget_tracker"
mongo = PyMongo(app)

@app.route('/')
def index():
    return 'Welcome to Budget Tracker'

if __name__ == '__main__':
    app.run(debug=True)
