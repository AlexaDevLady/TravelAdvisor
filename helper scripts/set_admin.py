from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt

client = MongoClient('mongodb+srv://adefelashogbanmu:uLo131XaLq1RZhEN@cluster0.ecs1xfy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0') 
db = client['travel_blog']
users_col = db['users']

username = 'sungjinwoo'
password = 'shadowMonarch'

existing = users_col.find_one({'username': username})
if existing:
    print(f"⚠️ User '{username}' already exists.")
else:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_col.insert_one({
        'username': username,
        'password': hashed,
        'role': 'admin'
    })
    print(f"✅ Admin user '{username}' created successfully.")
