# Description
アバターをブラウザで表示

# DB
room_id int | room_name varchar(10) | model_path varchar(20) | background_path varchar(20) | sound_path varchar(20) | vmd_path varchar(20) |  subtitle_path varchar(20)

idのみint, 他varchar

```
create table room_info(room_id int, room_name varchar(10), model_path varchar(20), background_path varchar(20), sound_path varchar(20), vmd_path varchar(20), subtitle_path varchar(20) );
```

```
insert into room_info values (1, 'sample_room', 'path/to/model/', 'path/to/bg/', 'path/to/sound/', 'path/to/vmd', 'path/to/subtitle');
```

# System
## RoomCreate
- room_nameなどを入力
- room_nameが使用可能か判定
- DBに保存
- Vstudio(?room_name=hogehoge)に遷移
- (できれば)ajaxでモデルをリアルタイム表示
- (できれば)編集パスワードもDBに保存

## Vstudio(?room_name)
- 録画開始ボタンを表示
- jsで録画＆録音
- 録画中はタイマーを表示
- 終わったらPythonで処理
- それか直接vmdを貼り付け
- vmdを得たらDBに保存

## Vroom(?room_name)
- DBからroom_nameに対応する各種データを取り出し
- それを使い, Three.jsでroomを表示

# todo
- app.py内のurlを動的に
- カメラ＆マイク
- qrコード