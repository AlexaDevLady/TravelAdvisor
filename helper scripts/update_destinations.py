from pymongo import MongoClient

# Replace this with your actual Mongo URI
MONGO_URI = 'mongodb+srv://adefelashogbanmu:uLo131XaLq1RZhEN@cluster0.ecs1xfy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(MONGO_URI)
db = client['travel_blog']
destinations_col = db['destinations']

def reset_destinations():
    print("⚠️  This will delete all current destinations and insert updated ones.")
    confirm = input("Type 'yes' to proceed: ")
    if confirm.lower() != 'yes':
        print("❌ Aborted.")
        return

    destinations_col.delete_many({})
    updated_destinations = [
        {
            'name': 'Paris',
            'description': 'The city of lights and love.',
            'image': 'paris.jpg',
            'lat': 48.8566,
            'lon': 2.3522
        },
        {
            'name': 'Tokyo',
            'description': 'A blend of tradition and modern life.',
            'image': 'japan.jpg',
            'lat': 35.6895,
            'lon': 139.6917
        },
        {
            'name': 'New York',
            'description': 'The city that never sleeps.',
            'image': 'new-york.jpg',
            'lat': 40.7128,
            'lon': -74.0060
        }
    ]
    destinations_col.insert_many(updated_destinations)
    print("✅ Destination data has been reset.")

def update_existing_destinations():
    print("🛠 Updating existing destinations without deleting.")
    updates = {
        'Paris': {'image': 'paris.jpg', 'lat': 48.8566, 'lon': 2.3522},
        'Tokyo': {'image': 'japan.jpg', 'lat': 35.6895, 'lon': 139.6917},
        'New York': {'image': 'new-york.jpg', 'lat': 40.7128, 'lon': -74.0060}
    }

    for name, fields in updates.items():
        result = destinations_col.update_one({'name': name}, {'$set': fields})
        print(f"🔄 Updated {name} ({'matched' if result.matched_count else 'not found'})")

    print("✅ Update completed.")

if __name__ == '__main__':
    print("1. Reset destinations (delete all and reinsert)")
    print("2. Update existing destination fields only")
    choice = input("Select an option (1 or 2): ")

    if choice == '1':
        reset_destinations()
    elif choice == '2':
        update_existing_destinations()
    else:
        print("❌ Invalid selection.")
