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