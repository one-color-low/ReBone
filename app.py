from flask import Flask, render_template, request, url_for
import os
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)

# ツール

def get_path(type, name):
    if type == "model":
        # pmd or pmxで場合分けする必要がある
        if name == "miku_1":
            return 'static/models/'+name+'/'+name+'.pmd'
        else:
            return 'static/models/'+name+'/'+name+'.pmx'
    elif type == "background":
        return 'static/backgrounds/'+name+'.jpg'
    elif type == "sound":
        return 'static/sounds/'+name+'.mp3'
    elif type == "vmd":
        return 'static/vmds/'+name+'.vmd'
    elif type == "subtitle":
        return 'static/subtitles/'+name+'.json'

def is_valid(room_name):    
    table = Entry.query.all()
    for row in table:
        if row.room_name == room_name:
            return False
    return True

def is_exist(room_name):
    table = Entry.query.all()
    for row in table:
        if row.room_name == room_name:
            return True
    return False

# ルーティング
@app.route('/', methods=['GET','POST'])
def createroom():
    if request.method == 'POST':
        if(is_valid(request.form["room_name"])):
            add_entry(
                room_name = request.form["room_name"], 
                model_path = get_path('model', request.form["model"]),
                background_path = get_path('background', request.form["background"]),
                sound_path = "", vmd_path = "", subtitle_path = "") 
            next_url = url_for('Vstudio', room_name=request.form["room_name"])
            return render_template('show_link_and_QRcode.html', url=next_url)
        else:
            return render_template('createroom.html', pre_val=request.form, message="このルーム名は既に使われています。")
    else:
        return render_template('createroom.html', pre_val=[], message = "")


@app.route('/Vstudio', methods=['POST', 'GET'])

def Vstudio():
    if is_exist(request.args.get('room_name','')):
        if request.method == 'POST':
            update_entry(
                room_name = request.args.get('room_name',''), 
                model_path = None,
                background_path = None,
                sound_path = get_path('sound', request.form['sound']), 
                vmd_path = get_path('vmd', request.form['vmd']),
                subtitle_path = get_path('subtitle', 'sample')) 
            next_url = url_for('Vroom',room_name=request.args.get('room_name'))
            return render_template('show_link_and_QRcode.html', url=next_url)
        else: 
            return render_template('Vstudio.html')
    else: 
        return render_template('not_found.html', message="ルームが指定されていないか、指定のルームが見つかりません。")
    

@app.route('/Vroom', methods=['POST', 'GET'])
def Vroom():
    if is_exist(request.args.get('room_name')):
        entry = Entry.query.filter(Entry.room_name == request.args.get('room_name') ).first()
        return render_template('Vroom.html', 
            model_path = entry.model_path,
            background_path = entry.background_path,
            sound_path = entry.sound_path,
            vmd_path = entry.vmd_path,
            subtitle_path = entry.subtitle_path )
    else:
        room_list = get_list_from_db()
        return render_template('list.html', room_list=room_list)


@app.route('/runanime')
def runanime():
    return render_template('runanime.html') 
 

# データベース
#db_uri = os.environ.get('DATABASE_URL') or "postgresql://localhost/flaskvtube"
db_uri = "sqlite:///" + os.path.join(app.root_path, 'flaskvtube.db') # 追加
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app) 

class Entry(db.Model): 
    __tablename__ = "rooms2" 
    room_name = db.Column(db.String(), primary_key=True) 
    model_path = db.Column(db.String(), nullable=False) 
    background_path = db.Column(db.String(), nullable=False) 
    sound_path = db.Column(db.String(), nullable=False) 
    vmd_path = db.Column(db.String(), nullable=False) 
    subtitle_path = db.Column(db.String(), nullable=False) 


def add_entry(room_name, model_path, background_path, sound_path, vmd_path, subtitle_path):
    entry = Entry()
    entry.room_name = room_name
    entry.model_path = model_path
    entry.background_path = background_path
    entry.sound_path = sound_path
    entry.vmd_path = vmd_path
    entry.subtitle_path = subtitle_path

    db.session.add(entry)
    db.session.commit()
    return 0

def update_entry(room_name, model_path, background_path, sound_path, vmd_path, subtitle_path):
    entry = Entry().query.filter(Entry.room_name == room_name).first()
    if model_path != None:
        entry.model_path = model_path
    if background_path != None:
        entry.background_path = background_path
    if sound_path != None:
        entry.sound_path = sound_path
    if vmd_path != None:
        entry.vmd_path = vmd_path
    if subtitle_path != None:
        entry.subtitle_path = subtitle_path

    db.session.add(entry)
    db.session.commit()
    return 0

# 実行
if __name__ == "__main__":
    app.run(debug=True)

# ※entry=一連の処理