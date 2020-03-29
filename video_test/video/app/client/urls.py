# coding:utf-8

from django.urls import path
from .views.base import Index
from .views.video import  CusVideo, VideoSub
from .views.auth import User, Regist, Logout
from .views.comment import CommentView


urlpatterns = [
  path('', Index.as_view(), name='client_index'),
  path('video/custom', CusVideo.as_view(), name='client_cus_video'),
  path('video/<int:video_id>', VideoSub.as_view(), name='client_video_sub'),
  path('auth', User.as_view(), name='client_auth'),
  path('auth/regist', Regist.as_view(), name='client_regist'),
  path('auth/logout', Logout.as_view(), name='client_logout'),
  path('comment/add', CommentView.as_view(), name='client_add_comment')
]
