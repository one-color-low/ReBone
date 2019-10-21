from flask import Flask, render_template, request
import os
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)

# ルーティング
@app.route('/createroom', methods=['POST', 'GET'])
def createroom():
    if request.method == 'POST':
        if(valid_rooom_name(request.form["room_name"])):
            return render_template('recording.html', model=request.form["model"], background=request.form["background"], room_name=request.form["room_name"])
        else:
            return render_template('createroom.html', message="このルーム名は既に使われています。")
    return render_template('createroom.html', message = "")

    def valid_rooom_name(room_name):    
        # todo: DBを参照してルーム名の重複を検知
        return True


@app.route('/Vroom', methods=['POST', 'GET'])
def Vroom():
    if request.method == 'GET':
        access_target_room(request.args.get)
    else:
        access_room_list()

    def access_target_room(room):
        # todo: DBからroomの各種データを取得
        model_path="/"
        background_path="/"
        vmd="sss"   # blobでデータベースに直接保存 or EC2のパス
        return render_template('Vroom.html',room_name=room, model_path=model_path, background_path=background_path, vmd=vmd )

    def access_room_list():
        # todo: DBから登録済みルーム一覧を取得
        room_list = ["aaa","bbb","ccc"]
        return render_template("Vroom_list.html", room_list=room_list)


@app.route('/runanime')
def runanime():
    return render_template('index.html') 
 

# データベース
db_uri = os.environ.get('DATABASE_URL') or "postgresql://localhost/flaskvtube"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app) 

class Entry(db.Model): 
    __tablename__ = "rooms" 
    room_id = db.Column(db.Integer, primary_key=True) 
    room_name = db.Column(db.String(), nullable=False) 
    model_path = db.Column(db.String(), nullable=False) 
    background_path = db.Column(db.String(), nullable=False) 
    sound_path = db.Column(db.String(), nullable=False) 
    vmd_path = db.Column(db.String(), nullable=False) 
    subtitle_path = db.Column(db.String(), nullable=False) 


@app.route('/')
def add_entry():
    entry = Entry()
    entry.room_id = 1
    entry.room_name = "oppai"
    entry.model_path = "path/to/model/"

    db.session.add(entry)
    db.session.commit()
    return render_template('sql_view.html', entry=entry)

def hello_world():
    entries = Entry.query.all() 
    return render_template('sql_view.html', entry=entries)

# 実行
if __name__ == "__main__":
    app.run(debug=True)