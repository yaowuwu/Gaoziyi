from django.db import models
from django.db import IntegrityError
# Create your models here.


class Swiper(models.Model):
    STYPES = (
        ('superlike', '上滑'),
        ('like', '右滑'),
        ('dislike', '左滑')
    )
    uid = models.IntegerField(verbose_name='滑动者ID')
    sid = models.IntegerField(verbose_name='被滑动者ID')
    stype = models.CharField(max_length=16, choices=STYPES, verbose_name='滑动的类型')
    stime = models.DateTimeField(auto_now_add=True, verbose_name='滑动时间')

    class Meta:
        unique_together = ['uid', 'sid']

    @classmethod
    def swipe(cls, uid, sid, stype):
        if stype not in ['like', 'superlike', 'dislike']:
            return '滑动类型错误'

        try:
            cls.objects.create(uid=uid, sid=sid, stype=stype)
        except IntegrityError:
            return '重复滑动'

    @classmethod
    def is_liked(cls, uid, sid):
        '''检查是否喜欢过某人'''
        like_styles = ['like', 'superlike']
        return cls.objects.filter(uid=uid, sid=sid, stype__in=like_styles).exists()


class Friend(models.Model):
    uid1 = models.IntegerField(verbose_name='好友ID')
    uid2 = models.IntegerField(verbose_name='好友ID')

    class Meta:
        unique_together = ['uid1', 'uid2']

    @staticmethod
    def sort_uid(uid1, uid2):
        if uid1 > uid2:
            return uid2, uid1
        else:
            return uid1, uid2

    @classmethod
    def make_friends(cls, uid1, uid2):
        uid1, uid2 = cls.sort_uid(uid1, uid2)
        return cls.objects.create(uid1=uid1, uid2=uid2)