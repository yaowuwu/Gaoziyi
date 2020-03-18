from django.db import models
from django.db import IntegrityError
from common import err
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
        '''增加一次滑动记录'''
        if stype not in ['like', 'superlike', 'dislike']:
            raise err.StypeErr('滑动类型错误')
        try:
            cls.objects.create(uid=uid, sid=sid, stype=stype)
        except IntegrityError:
            raise err.SwipeRepeatErr('重复滑动')

    @classmethod
    def is_liked(cls, uid, sid):
        '''检查是否喜欢过某人'''
        like_styles = ['like', 'superlike']
        try:
            swipe = cls.objects.get(uid=uid, sid=sid)
            return swipe.stype in like_styles
        except cls.DoesNotExist:
            return None


class Friend(models.Model):
    '''好友表'''
    uid1 = models.IntegerField(verbose_name='好友ID')
    uid2 = models.IntegerField(verbose_name='好友ID')

    class Meta:
        unique_together = ['uid1', 'uid2']

    @staticmethod
    def sort_uid(uid1, uid2):
        '''为uid排序'''
        if uid1 > uid2:
            return uid2, uid1
        else:
            return uid1, uid2

    @classmethod
    def make_friends(cls, uid1, uid2):
        '''建立好友关系'''
        uid1, uid2 = cls.sort_uid(uid1, uid2)
        try:
            return cls.objects.create(uid1=uid1, uid2=uid2)
        except IntegrityError:
            pass

    @classmethod
    def break_off(cls, uid1, uid2):
        '''解除好友关系'''
        uid1, uid2 = cls.sort_uid(uid1, uid2)
        cls.objects.filter(uid1=uid1, uid2=uid2).delete()

    @classmethod
    def friend_id_list(cls, uid):
        '''好友ID列表'''
        query_condition = models.Q(uid1=uid) | models.Q(uid2=uid)
        frd_record = cls.objects.filter(query_condition)
        fid_list = []
        for frd in frd_record:
            if frd.uid1 == uid:
                fid_list.append(frd.uid2)
            else:
                fid_list.append(frd.uid2)
        return fid_list