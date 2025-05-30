import os
from pymongo import MongoClient
from bson.objectid import ObjectId
import cloudinary
import cloudinary.uploader

# 1. Configure Cloudinary
cloudinary.config( 
    cloud_name = "dossuuyap", 
    api_key = "773232315157195", 
    api_secret = "dqlVfUTY4QTlY5a7DGtuMeXfZt8", # Click 'View API Keys' above to copy your API secret
    secure=True
)


# 2. Connect to MongoDB
client = MongoClient('mongodb+srv://adefelashogbanmu:uLo131XaLq1RZhEN@cluster0.ecs1xfy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0') 
db = client['travel_blog']
destinations_col = db['destinations']

# 3. Local static folder path
STATIC_IMAGE_FOLDER = os.path.join(os.getcwd(), 'static', 'images')

# 4. Process each destination
for dest in destinations_col.find():
    local_image = dest.get('image')

    # Skip if already a Cloudinary URL
    if local_image and local_image.startswith('http'):
        print(f"Skipping: {dest['name']} already has cloud URL.")
        continue

    local_path = os.path.join(STATIC_IMAGE_FOLDER, local_image)
    if not os.path.exists(local_path):
        print(f"File not found for: {local_image}")
        continue

    try:
        # 5. Upload to Cloudinary
        result = cloudinary.uploader.upload(local_path, folder='travel_blog/destinations')
        cloud_url = result['secure_url']

        # 6. Update MongoDB
        destinations_col.update_one(
            {'_id': dest['_id']},
            {'$set': {'image': cloud_url}}
        )

        print(f"Uploaded & updated: {dest['name']} → {cloud_url}")

    except Exception as e:
        print(f"Error uploading {local_image}: {e}")
