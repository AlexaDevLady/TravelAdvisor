from pymongo import MongoClient
from datetime import datetime
import hashlib

# MongoDB Setup
MONGO_URI = 'mongodb+srv://adefelashogbanmu:uLo131XaLq1RZhEN@cluster0.ecs1xfy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(MONGO_URI)
db = client['travel_blog']
blog_posts_col = db['blog_posts']

# Utility: Generate slug from title
def generate_slug(title):
    return title.lower().replace(" ", "-").replace("?", "").replace(",", "").replace(".", "").strip()

# Blog post data (you can edit this list as needed)
blog_posts = [
    {
        'title': 'Top 10 Travel Tips',
        'content': '## Packing\nAlways roll your clothes.',
        'category': 'Tips'
    },
    {
        'title': 'How to pack light',
        'content': '**Only take what you need.**',
        'category': 'Packing'
    },
    {
        'title': 'Best Destinations in 2024',
        'content': '*Visit* Bali, Japan, and Iceland.',
        'category': 'Destinations'
    },
    {
        'title': 'Budget Travel Guide',
        'content': 'Save more by booking early and using local transport.',
        'category': 'Budget'
    }
]

def update_or_insert_blog_posts():
    print("🔄 Updating or inserting blog posts...")
    for post in blog_posts:
        now = datetime.utcnow()
        slug = generate_slug(post['title'])
        update_data = {
            'content': post['content'],
            'category': post.get('category', 'General'),
            'slug': slug,
            'updated_at': now
        }

        existing = blog_posts_col.find_one({'title': post['title']})
        if existing:
            blog_posts_col.update_one(
                {'_id': existing['_id']},
                {'$set': update_data}
            )
            print(f"📝 Updated: {post['title']}")
        else:
            post['slug'] = slug
            post['created_at'] = now
            post['updated_at'] = now
            blog_posts_col.insert_one(post)
            print(f"✅ Inserted: {post['title']}")

if __name__ == '__main__':
    update_or_insert_blog_posts()
    print("🎉 Blog posts have been synced.")
