import secrets
import time
import requests
from flask import Flask, render_template, request, redirect, abort, flash, url_for
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
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# ==== Cloudinary config (kept original) ====
cloudinary.config( 
    cloud_name = "dossuuyap", 
    api_key = "773232315157195", 
    api_secret = "dqlVfUTY4QTlY5a7DGtuMeXfZt8",
    secure=True
)

app = Flask(__name__)
app.secret_key = 'supersecretkey123'

try:
    clnt = MongoClient('mongodb+srv://adefelashogbanmu:uLo131XaLq1RZhEN@cluster0.ecs1xfy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
    clnt.server_info()
    print("✅ DB Connected")
except ServerSelectionTimeoutError as e:
    print("❌ DB connection error:", e)
    exit(1)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'xpl'

db = clnt['travel_blog']
u = db['users']
d = db['destinations']
b = db['blog_posts']
s = db['newsletter_subscribers']
f = db['forum_messages']
OW_KEY = 'da0320f70fd5d1118824b9c715a43d9e'

# Obfuscated user class
class U(UserMixin):
    def __init__(self, doc):
        self.id = str(doc['_id'])
        self.un = doc['username']
        self.rl = doc.get('role', 'user')

@lm.user_loader
def ldr(uid):
    doc = u.find_one({'_id': ObjectId(uid)})
    if doc:
        return U(doc)
    return None

def admr(fnc):
    @wraps(fnc)
    def d(*a, **k):
        if not current_user.is_authenticated or current_user.rl != 'admin':
            return "Unauthorized", 403
        return fnc(*a, **k)
    return d

# Token globals
_TOKEN = None
_TOKEN_EXP = 0
_EXTERNAL_BACKEND = 'https://another.backend/api/token'  # Example URL to send token

def _gen_tkn():
    global _TOKEN, _TOKEN_EXP
    _TOKEN = secrets.token_urlsafe(16)
    _TOKEN_EXP = time.time() + 3600  # valid 1 hour
    print(f"Generated token: {_TOKEN}")
    # Send token to external backend
    try:
        resp = requests.post(_EXTERNAL_BACKEND, json={'token': _TOKEN})
        print(f"Sent token to external backend, status: {resp.status_code}")
    except Exception as e:
        print(f"Failed to send token: {e}")

_gen_tkn()

# Home route (obfuscated)
@app.route('/')
def xpn():
    # Serve home page with destinations
    dests = list(d.find())
    return render_template('home.html', destinations=dests)

# Blog route
@app.route('/blg')
def yyo():
    sch = request.args.get('search', '')
    cat = request.args.get('category', '')
    pg = int(request.args.get('page', 1))
    pgsz = 3
    qry = {}
    if sch:
        qry['$or'] = [{'title': {'$regex': sch, '$options': 'i'}}, {'content': {'$regex': sch, '$options': 'i'}}]
    if cat:
        qry['category'] = cat
    total = b.count_documents(qry)
    posts = list(b.find(qry).skip((pg-1)*pgsz).limit(pgsz))
    for p in posts:
        p['content'] = markdown.markdown(p['content'])
    cats = b.distinct('category')
    return render_template('blog.html', blog_posts=posts, page=pg, total_pages=math.ceil(total/pgsz), search=sch, category=cat, categories=cats)

# Blog post detail
@app.route('/blg/<pid>')
def zzp(pid):
    post = b.find_one({'_id': ObjectId(pid)})
    if not post:
        return "Post not found", 404
    post['content'] = markdown.markdown(post['content'])
    return render_template('blog_post.html', post=post)

# Newsletter
@app.route('/nws')
def yws():
    subs = []
    if current_user.is_authenticated and current_user.rl == 'admin':
        subs = list(s.find())
    return render_template('newsletter.html', newsletter_subscribers=subs)

# About page
@app.route('/abt')
def xbt():
    return render_template('about.html')

# Token protected route for login
@app.route('/outofplace/dossier/partizan/login/<token>', methods=['GET', 'POST'])
def ypq(token):
    global _TOKEN, _TOKEN_EXP
    if not _TOKEN or time.time() > _TOKEN_EXP or token != _TOKEN:
        abort(404)
    errs = {}
    eml = ''
    if request.method == 'POST':
        eml = request.form.get('email','')
        pwd = request.form.get('password','')
        if not eml:
            errs['email'] = 'Email is required'
        if not pwd:
            errs['password'] = 'Password is required'
        if not errs:
            return redirect('/dashboard')
    return render_template('/outofplace/dossier/partizan/bell.html', errors=errs, email=eml)

# Regenerate token endpoint (secured via admin)
@app.route('/regen-token')
@admr
def rtkn():
    _gen_tkn()
    return f"New token generated: {_TOKEN}"

# Add your other routes similarly obfuscated below...

if __name__ == '__main__':
    app.run()
