# coding:utf-8

import os
import time
import shutil

from django.conf import settings
from app.models import Video, VideoSub
from app.tasks.task import video_task
from app.libs.base_qiniu import video_qiniu




def check_and_get_video_type(type_obj, type_value, message):
    try:
        type_obj(type_value)
    except:
        return {'code': -1, 'msg': message}

    return {'code': 0, 'msg': 'success'}


def remove_path(paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)

def remove_path(paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)

def handle_video(video_file, video_id, number):

    in_path = os.path.join(settings.BASE_DIR, 'app/dashboard/temp_in')
    out_path = os.path.join(settings.BASE_DIR, 'app/dashboard/temp_out')
    name = '{}_{}'.format(int(time.time()), video_file.name)
    path_name = '/'.join([in_path, name])

    temp_path = video_file.temporary_file_path()

    shutil.copyfile(temp_path, path_name)

    out_name = '{}_{}'.format(int(time.time()), video_file.name.split('.')[0])
    out_path = '/'.join([out_path, out_name])
    print("path_name: ",in_path)
    print("out_path: ",out_path)
    command = 'D:/ffmpeg/ffmpeg-20200324-e5d25d1-win64-static/bin/ffmpeg -i {} -c copy {}.mp4'.format(path_name, out_path)

    os.system(command)
    out_name='.'.join([out_path,'mp4'])
    if not os.path.exists(out_name):
        remove_path([out_name, path_name])
        return False
    url = video_qiniu.put(video_file.name,out_name)
    if url:
        video = Video.objects.get(pk=video_id)
        try:
            VideoSub.objects.create(
                video = video,
                url = url,
                number = number
            )
            return  True
        except:
            return False
        finally:
            remove_path([out_name,path_name])
    return False
    # video = Video.objects.get(pk=video_id)
    # video_sub = VideoSub.objects.create(
    #     video=video,
    #     url='',
    #     number=number
    # )
    #
    # video_task.delay(
    #     command, out_path, path_name, video_file.name, video_sub.id)


   # print("url= ",url)

