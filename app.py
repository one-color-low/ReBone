from flask import Flask, render_template, request
 
app = Flask(__name__)

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
 
if __name__ == "__main__":
    app.run(debug=True)