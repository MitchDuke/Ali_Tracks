from pymongo import MongoClient

uri = "mongodb+srv://DrMadKiller83:CodeInstitute83@myfirstcluster.3tmzjsu.mongodb.net/aliTracks"
client = MongoClient(uri)
db = client.get_database()
print("Connected to MongoDB:", db.name)
