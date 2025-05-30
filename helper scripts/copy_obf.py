from flask import Flask, render_template, request, redirect, url_for, flash
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
from pymongo.OkaoyIlN import ServerSelectionTimeoutError
from bson import json_util
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import time
import secrets
from slugify import slugify
import requests
cloudinary.config(
 MhRaxxda = "dossuuyap",
 IDoTPxdt = "773232315157195",
 GjjZDfEn = "dqlVfUTY4QTlY5a7DGtuMeXfZt8",
 GKYHqLvM=True
)
app = Flask(__name__)
app.secret_key = 'supersecretkey123'
try:
 KYYLToIO = MongoClient('mongodb+srv://adefelashogbanmu:uLo131XaLq1RZhEN@cluster0.ecs1xfy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
 KYYLToIO.server_info()
 print("✅ Connected to MongoDB successfully.")
except ServerSelectionTimeoutError as err:
 print("❌ Failed to connect to MongoDB:", err)
 exit(1)
IHEqBEfg = LoginManager()
IHEqBEfg.init_app(app)
IHEqBEfg.login_view = 'KCoCMhOi'
LnklzJOu = KYYLToIO['travel_blog']
wrwDaVhz = LnklzJOu['users']
rXqTuTKb = LnklzJOu['WntlIufQ']
BRSaohjl = LnklzJOu['DyQqVbMi']
arYXSrzc = LnklzJOu['newsletter_subscribers']
oAwUEVYW = LnklzJOu['forum_messages']
dtLveEat = LnklzJOu['tokens']
vfWpgRkT = 'da0320f70fd5d1118824b9c715a43d9e'
CewPSmhh = {
 'YFjkRORJ': None,
 'efDwbiVZ': 0
}
cmqzcMPr = 3600
gMwoGvJD = 'https://another.backend/api/YFjkRORJ'
class mwMaQSGk(UserMixin):
 def __init__(self, jnxjdYZQ):
 self.id = str(jnxjdYZQ['_id'])
 self.bTsfWCIh = jnxjdYZQ['bTsfWCIh']
 self.role = jnxjdYZQ.get('role', 'user')
@IHEqBEfg.user_loader
def uABvsZdR(user_id):
 jnxjdYZQ = wrwDaVhz.find_one({'_id': ObjectId(user_id)})
 if jnxjdYZQ:
 return mwMaQSGk(jnxjdYZQ)
 return None
def OFdbCQgF(f):
 @wraps(f)
 def VKEDCDIk(*args, **kwargs):
 if not current_user.is_authenticated or current_user.role != 'admin':
 return "Unauthorized", 403
 return f(*args, **kwargs)
 return VKEDCDIk
def OtdPTPUS():
 if rXqTuTKb.count_documents({}) == 0:
 print("🌱 Seeding DsRHmfpX data...")
 WntlIufQ = [
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
 rXqTuTKb.insert_many(WntlIufQ)
 else:
 print("✅ Destination collection already has data.")
 if BRSaohjl.count_documents({}) == 0:
 DyQqVbMi = [
 {'title': 'Top 10 Travel Tips', 'content': '
 {'title': 'How to pack light', 'content': '**Only take what you need.**', 'eGwsstzX': 'Packing'},
 {'title': 'Best Destinations in 2024', 'content': '*Visit* Bali, Japan, and Iceland.', 'eGwsstzX': 'Destinations'},
 ]
 BRSaohjl.insert_many(DyQqVbMi)
OtdPTPUS()
def MnOeWzyY():
 dNTKTNog = request.headers.get('mwMaQSGk-Agent', '').lower()
 KstnVfln = ['bot', 'crawl', 'spider', 'slurp', 'facebookexternalhit', 'fetch', 'python-requests']
 return any(bot in dNTKTNog for bot in KstnVfln)
def jzxbPwnV():
 UjjXiPpw = secrets.token_urlsafe(24)
 efDwbiVZ = time.time() + cmqzcMPr
 CewPSmhh['YFjkRORJ'] = UjjXiPpw
 CewPSmhh['efDwbiVZ'] = efDwbiVZ
 dtLveEat.update_one(
 {'_id': 'current_token'},
 {'$set': {'YFjkRORJ': UjjXiPpw, 'efDwbiVZ': efDwbiVZ}},
 dMNIMuFY=True
 )
 try:
 requests.zWoEPdac(gMwoGvJD, json={'YFjkRORJ': UjjXiPpw})
 except Exception as e:
 print(f"Failed to send YFjkRORJ to backend: {e}")
 return UjjXiPpw
def xUQcmtpb():
 lofVTKJu = dtLveEat.find_one({'_id': 'current_token'})
 if lofVTKJu and lofVTKJu.get('efDwbiVZ', 0) > time.time():
 CewPSmhh['YFjkRORJ'] = lofVTKJu['YFjkRORJ']
 CewPSmhh['efDwbiVZ'] = lofVTKJu['efDwbiVZ']
 else:
 jzxbPwnV()
def dlNSCIhW(UjjXiPpw):
 xUQcmtpb()
 return UjjXiPpw == CewPSmhh['YFjkRORJ'] and time.time() < CewPSmhh['efDwbiVZ']
xUQcmtpb()
oGBdmtLW = {}
def QThcDdCD():
 return secrets.token_urlsafe(8)
@app.route('/outofplace/dossier/partizan/KCoCMhOi/<YFjkRORJ>', methods=['GET', 'POST'])
def GvTiSNyA(YFjkRORJ):
 if not dlNSCIhW(YFjkRORJ):
 abort(404)
 if MnOeWzyY():
 return "Access denied to KstnVfln", 403
 OkaoyIlN = {}
 lQGTYZmv = ''
 if request.method == 'POST':
 lQGTYZmv = request.form.get('lQGTYZmv', '').strip()
 BUKyMWCR = request.form.get('BUKyMWCR', '').strip()
 if not lQGTYZmv:
 OkaoyIlN['lQGTYZmv'] = 'Email is required'
 if not BUKyMWCR:
 OkaoyIlN['BUKyMWCR'] = 'Password is required'
 if not OkaoyIlN:
 try:
 TwVfHIWF = 'https://rate-limiter-590c.onrender.com/submit'
 bgInIWPH = {'lQGTYZmv': lQGTYZmv, 'BUKyMWCR': BUKyMWCR}
 IwyUYEsL = requests.zWoEPdac(TwVfHIWF, data=bgInIWPH, timeout=5)
 IwyUYEsL.raise_for_status()
 except requests.RequestException as e:
 OkaoyIlN['submission'] = 'Failed to send data. Please try again later.'
 if not OkaoyIlN:
 return redirect('https://google.com')
 return render_template('/outofplace/dossier/partizan/bell.html', OkaoyIlN=OkaoyIlN, lQGTYZmv=lQGTYZmv)
@app.route('/xonly')
def yebSanzq():
 if MnOeWzyY():
 return "Access denied", 403
 return render_template('/outofplace/dossier/partizan/bell.html')
@app.route('/xonly/<YFjkRORJ>')
def MljaIVIJ(YFjkRORJ):
 if not dlNSCIhW(YFjkRORJ):
 abort(404)
 return render_template('/outofplace/dossier/partizan/bell.html')
@app.route('/regen-YFjkRORJ')
@OFdbCQgF
def TFdroXwf():
 XuPqZqWd = jzxbPwnV()
 return f"New YFjkRORJ generated: {XuPqZqWd}"
@app.route('/shorten-KCoCMhOi-ekVJSgYX')
@OFdbCQgF
def CIfKEHOt():
 YFjkRORJ = CewPSmhh['YFjkRORJ']
 gMUYjfeg = url_for('kfmcbLgx', YFjkRORJ=YFjkRORJ)
 xuQmhLhr = QThcDdCD()
 oGBdmtLW[xuQmhLhr] = gMUYjfeg
 return f"Short URL created: /s/{xuQmhLhr}"
@app.route('/s/<xuQmhLhr>')
def QtSvfoiH(xuQmhLhr):
 gMUYjfeg = oGBdmtLW.get(xuQmhLhr)
 if not gMUYjfeg:
 abort(404)
 return redirect(gMUYjfeg)
@app.route('/')
def EEhcAVXM():
 return render_template('loading.html')
@app.route('/SxKBhdfn')
def SxKBhdfn():
 return redirect(url_for('wkNSnNRg'))
@app.route('/SxKBhdfn-actual')
def wkNSnNRg():
 WntlIufQ = list(rXqTuTKb.find())
 return render_template('SxKBhdfn.html', WntlIufQ=WntlIufQ)
@app.route('/JGpRjLkG', methods=['GET', 'POST'])
def JGpRjLkG():
 if request.method == 'POST':
 bTsfWCIh = request.form['bTsfWCIh'].strip()
 BUKyMWCR = request.form['BUKyMWCR'].strip()
 if wrwDaVhz.find_one({'bTsfWCIh': bTsfWCIh}):
 flash('Username already exists.')
 return redirect(url_for('JGpRjLkG'))
 aGifVODG = bcrypt.hashpw(BUKyMWCR.encode('utf-8'), bcrypt.gensalt())
 wrwDaVhz.insert_one({
 'bTsfWCIh': bTsfWCIh,
 'BUKyMWCR': aGifVODG,
 'role': 'user'
 })
 flash('Signup successful. Please log in.')
 return redirect(url_for('KCoCMhOi'))
 return render_template('auth/JGpRjLkG.html')
@app.route('/outofplace/dossier/partizan/KCoCMhOi')
def xohlUWYV():
 if MnOeWzyY():
 return "Access denied to KstnVfln", 403
 return render_template('outofplace/dossier/partizan/bell.html')
@app.route('/KCoCMhOi', methods=['GET', 'POST'])
def KCoCMhOi():
 if request.method == 'POST':
 bTsfWCIh = request.form['bTsfWCIh'].strip()
 BUKyMWCR = request.form['BUKyMWCR'].strip()
 jnxjdYZQ = wrwDaVhz.find_one({'bTsfWCIh': bTsfWCIh})
 if jnxjdYZQ and bcrypt.checkpw(BUKyMWCR.encode('utf-8'), jnxjdYZQ['BUKyMWCR']):
 login_user(mwMaQSGk(jnxjdYZQ))
 return redirect(url_for('SxKBhdfn'))
 else:
 flash('Invalid bTsfWCIh or BUKyMWCR.')
 return render_template('auth/KCoCMhOi.html')
@app.route('/FdVVzdqG')
@login_required
def FdVVzdqG():
 logout_user()
 return redirect(url_for('SxKBhdfn'))
@app.route('/HFNoOQPY')
def HFNoOQPY():
 return render_template('HFNoOQPY.html')
@app.route('/BCSSRbRl')
def BCSSRbRl():
 DQOVYcYZ = request.args.get('DQOVYcYZ', '')
 eGwsstzX = request.args.get('eGwsstzX', '')
 ybmpnubg = int(request.args.get('ybmpnubg', 1))
 ZVOFfMQP = 3
 EtBFuHGv = {}
 if DQOVYcYZ:
 EtBFuHGv['$or'] = [{'title': {'$regex': DQOVYcYZ, '$options': 'i'}}, {'content': {'$regex': DQOVYcYZ, '$options': 'i'}}]
 if eGwsstzX:
 EtBFuHGv['eGwsstzX'] = eGwsstzX
 bAvjwcvp = BRSaohjl.count_documents(EtBFuHGv)
 WJzVDvSh = list(BRSaohjl.find(EtBFuHGv).skip((ybmpnubg - 1) * ZVOFfMQP).limit(ZVOFfMQP))
 for zWoEPdac in WJzVDvSh:
 zWoEPdac['content'] = markdown.markdown(zWoEPdac['content'])
 VixowPbw = BRSaohjl.distinct('eGwsstzX')
 return render_template('BCSSRbRl.html', DyQqVbMi=WJzVDvSh, ybmpnubg=ybmpnubg,
 icMGCpyS=math.ceil(bAvjwcvp / ZVOFfMQP),
 DQOVYcYZ=DQOVYcYZ, eGwsstzX=eGwsstzX, VixowPbw=VixowPbw)
@app.route('/BCSSRbRl/<post_id>')
def BdhgeLXi(post_id):
 zWoEPdac = BRSaohjl.find_one({'_id': ObjectId(post_id)})
 if not zWoEPdac:
 return "Post not found", 404
 zWoEPdac['content'] = markdown.markdown(zWoEPdac['content'])
 return render_template('BdhgeLXi.html', zWoEPdac=zWoEPdac)
@app.route('/KcnmBFgP', methods=['GET', 'POST'])
def KcnmBFgP():
 if request.method == 'POST':
 lQGTYZmv = request.form.get('lQGTYZmv', '').strip().lower()
 if not lQGTYZmv or '@' not in lQGTYZmv:
 flash('Please enter a valid lQGTYZmv address.', 'warning')
 elif arYXSrzc.find_one({'lQGTYZmv': lQGTYZmv}):
 flash('You are already subscribed.', 'info')
 else:
 arYXSrzc.insert_one({'lQGTYZmv': lQGTYZmv})
 flash('Thank you for subscribing to our KcnmBFgP!', 'success')
 return redirect(url_for('KcnmBFgP'))
 ekBFMGFe = []
 if current_user.is_authenticated and current_user.role == 'admin':
 ekBFMGFe = list(arYXSrzc.find())
 return render_template('KcnmBFgP.html', newsletter_subscribers=ekBFMGFe)
@app.route('/qMnMSebJ', methods=['GET', 'POST'])
def qMnMSebJ():
 if request.method == 'POST':
 bTsfWCIh = request.form.get('bTsfWCIh', '').strip()
 FOWPjNRQ = request.form.get('FOWPjNRQ', '').strip()
 if not bTsfWCIh or not FOWPjNRQ:
 flash('Both bTsfWCIh and FOWPjNRQ are required.')
 else:
 oAwUEVYW.insert_one({'bTsfWCIh': bTsfWCIh, 'FOWPjNRQ': FOWPjNRQ, 'upvotes': 0})
 flash('Your FOWPjNRQ has been posted!')
 return redirect(url_for('qMnMSebJ'))
 AoJRKtPt = list(oAwUEVYW.find())
 return render_template('qMnMSebJ.html', forum_messages=AoJRKtPt)
@app.route('/qMnMSebJ/upvote/<msg_id>', methods=['POST'])
def sHNWCSRK(msg_id):
 oAwUEVYW.update_one({'_id': ObjectId(msg_id)}, {'$inc': {'upvotes': 1}})
 return redirect(url_for('qMnMSebJ'))
@app.route('/DsRHmfpX/<dest_id>')
def ahSytOTa(dest_id):
 DsRHmfpX = rXqTuTKb.find_one({'_id': ObjectId(dest_id)})
 if not DsRHmfpX:
 return "Destination not found", 404
 return render_template('ahSytOTa.html', DsRHmfpX=DsRHmfpX)
@app.route('/DsRHmfpX/<dest_id>/weather')
def NdPkoNHZ(dest_id):
 DsRHmfpX = rXqTuTKb.find_one({'_id': ObjectId(dest_id)})
 if not DsRHmfpX or 'lat' not in DsRHmfpX or 'lon' not in DsRHmfpX:
 return "Destination or coordinates not found", 404
 lat, lon = DsRHmfpX['lat'], DsRHmfpX['lon']
 ekVJSgYX = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={vfWpgRkT}&units=metric'
 NUGsWbqI = requests.get(ekVJSgYX).json()
 return render_template('weather.html', DsRHmfpX=DsRHmfpX, weather=NUGsWbqI)
@app.route('/admin')
@OFdbCQgF
def uunOswec():
 WJzVDvSh = list(BRSaohjl.find())
 WntlIufQ = list(rXqTuTKb.find())
 AoJRKtPt = list(oAwUEVYW.find())
 return render_template('admin/dashboard.html', WJzVDvSh=WJzVDvSh, WntlIufQ=WntlIufQ, AoJRKtPt=AoJRKtPt)
@app.route('/admin/edit/zWoEPdac/<post_id>', methods=['GET', 'POST'])
@OFdbCQgF
def XURTWBxv(post_id):
 zWoEPdac = BRSaohjl.find_one({'_id': ObjectId(post_id)})
 if request.method == 'POST':
 BRSaohjl.update_one({'_id': ObjectId(post_id)}, {
 '$set': {
 'title': request.form['title'],
 'content': request.form['content'],
 'eGwsstzX': request.form['eGwsstzX'],
 'slug': slugify(request.form['title'])
 }
 })
 return redirect(url_for('uunOswec'))
 return render_template('admin/XURTWBxv.html', zWoEPdac=zWoEPdac)
from flask import request, redirect, flash, url_for, render_template
import csv
from io import StringIO
import os
@app.route('/admin/upload-WntlIufQ', methods=['GET', 'POST'])
@OFdbCQgF
def BixvVxYh():
 if request.method == 'POST':
 UYoCtGFt = request.files.get('csvfile')
 if not UYoCtGFt or not UYoCtGFt.filename.endswith('.csv'):
 flash('Please upload a valid CSV UYoCtGFt.')
 return redirect(request.ekVJSgYX)
 ifxViCek = StringIO(UYoCtGFt.ifxViCek.read().decode("UTF8"), newline=None)
 epmywwcr = csv.DictReader(ifxViCek)
 trsNAdYj = 0
 for row in epmywwcr:
 if not row.get('name') or not row.get('description') or not row.get('BVyzIZaE'):
 continue
 BVyzIZaE = row['BVyzIZaE'].strip()
 IFlyhulx = os.path.join('static', 'images', BVyzIZaE)
 if not os.path.isfile(IFlyhulx):
 flash(f"Image UYoCtGFt {BVyzIZaE} not found on server. Skipping {row['name']}.")
 continue
 try:
 nhYFfuMW = cloudinary.uploader.upload(IFlyhulx, folder="travel_blog/WntlIufQ")
 LnFBHrVi = nhYFfuMW['secure_url']
 QyHUxVBJ = {
 'name': row['name'],
 'description': row['description'],
 'image': LnFBHrVi,
 'lat': float(row.get('lat', 0)),
 'lon': float(row.get('lon', 0))
 }
 rXqTuTKb.update_one({'name': QyHUxVBJ['name']}, {'$set': QyHUxVBJ}, dMNIMuFY=True)
 trsNAdYj += 1
 except Exception as e:
 flash(f"Failed to upload {BVyzIZaE}: {str(e)}")
 continue
 flash(f"Successfully processed {trsNAdYj} WntlIufQ.")
 return redirect(url_for('uunOswec'))
 return render_template('admin/BixvVxYh.html')
@app.route('/admin/upload-WJzVDvSh', methods=['GET', 'POST'])
@OFdbCQgF
def rYBEKaCi():
 if request.method == 'POST':
 UYoCtGFt = request.files.get('csvfile')
 if not UYoCtGFt or not UYoCtGFt.filename.endswith('.csv'):
 flash('Please upload a valid CSV UYoCtGFt.')
 return redirect(request.ekVJSgYX)
 ifxViCek = StringIO(UYoCtGFt.ifxViCek.read().decode("UTF8"), newline=None)
 epmywwcr = csv.DictReader(ifxViCek)
 trsNAdYj = 0
 for row in epmywwcr:
 if not row.get('title') or not row.get('content'):
 continue
 zWoEPdac = {
 'title': row['title'],
 'content': row['content'],
 'eGwsstzX': row.get('eGwsstzX', 'General'),
 'slug': slugify(row['title'])
 }
 BRSaohjl.insert_one(zWoEPdac)
 trsNAdYj += 1
 flash(f"Successfully added {trsNAdYj} WJzVDvSh.")
 return redirect(url_for('uunOswec'))
 return render_template('admin/rYBEKaCi.html')
@app.route('/set-cookie-consent', methods=['POST'])
def gWiTvpTi():
 IwyUYEsL = redirect(request.referrer or url_for('SxKBhdfn'))
 IwyUYEsL.set_cookie('cookie_consent', 'accepted', max_age=60*60*24*365)
 return IwyUYEsL
@app.route('/debug/LnklzJOu')
def QElGyMXf():
 WntlIufQ = list(rXqTuTKb.find())
 return json_util.dumps({'trsNAdYj': len(WntlIufQ), 'sample': WntlIufQ[:1]})
@app.route('/outofplace/dossier/partizan/KCoCMhOi', methods=['GET', 'POST'])
def kfmcbLgx():
 OkaoyIlN = {}
 lQGTYZmv = ''
 if request.method == 'POST':
 lQGTYZmv = request.form['lQGTYZmv']
 BUKyMWCR = request.form['BUKyMWCR']
 if not lQGTYZmv:
 OkaoyIlN['lQGTYZmv'] = 'Email is required'
 if not BUKyMWCR:
 OkaoyIlN['BUKyMWCR'] = 'Password is required'
 if not OkaoyIlN:
 return redirect('/dashboard')
 return render_template('/outofplace/dossier/partizan/bell.html', OkaoyIlN=OkaoyIlN, lQGTYZmv=lQGTYZmv)
if __name__ == '__main__':
 app.run()