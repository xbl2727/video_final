# coding:utf-8

from enum import Enum
from django.db import models


class VideoType(Enum):
    input = 'input'
    output = 'output'

VideoType.input.label = '原版'
VideoType.output.label = '输出'


class Video(models.Model):
    name = models.CharField(max_length=100, default='')
    video_type = models.CharField(max_length=50, default=VideoType.input.value)
    status = models.BooleanField(default=True, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    from_user = models.CharField(max_length=100, default='')
    url = models.CharField(max_length=500,default='' )

    class Meta:
        index_together = ('name', 'video_type', 'from_user')
        #联合索引，联合同步查询，提高效率
        #unique_together :联合约束，不能重复，不能一样

    def __str__(self):
        return self.name


class VideoStar(models.Model):
    video = models.ForeignKey(
        Video,
        related_name='video_star',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    name = models.CharField(max_length=100, null=False)
    identity = models.CharField(max_length=50, default='')

    class Meta:
        unique_together = ('video', 'name', 'identity')

    @property
    def ident(self):
        try:
            result = IdentityType(self.identity)
        except:
            return ''
        return result.label

    def __str__(self):
        return self.name


class VideoSub(models.Model):
    video = models.ForeignKey(
        Video,
        related_name='video_sub',
        on_delete=models.SET_NULL,
        blank=True, null=True
    )
    url = models.CharField(max_length=500, null=False)
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ('video', 'number')

    def __str__(self):
        return 'video:{}, number:{}'.format(self.video.name, self.number)
