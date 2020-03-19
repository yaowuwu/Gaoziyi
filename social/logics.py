import datetime

from django.db.transaction import atomic

from user.models import User
from social.models import Swiper
from social.models import Friend
from common import err
from common import keys
from libs.cache import rds


def rcmd_users_from_q(uid):
    '''从优先队列中获取推荐对象'''
    name = keys.FIRST_RCMD_Q % uid
    uid_list = rds.lrange(name, 0, 24)
    uid_list = [int(uid) for uid in uid_list]
    return User.objects.filter(id__in=uid_list)


def rcmd_users_from_db(uid, num, ):
    '''为用户推荐一些可以交友的对象'''
    user = User.objects.get(id=uid)
    today = datetime.date.today()

    # 计算目标人群的出生日期范围
    earliest_birthday = today - datetime.timedelta(user.profile.max_dating_age * 365)
    latest_birthday = today - datetime.timedelta(user.profile.min_dating_age * 365)

    # 取出所有已滑过的用户的 ID 列表
    sid_list = Swiper.objects.filter(uid=uid).values_list('sid', flat=True)

    # 从数据库中获取目标用户
    users = User.objects.filter(
        gender=user.profile.dating_gender,
        location=user.profile.dating_location,
        birthday__gte=earliest_birthday,
        birthday__lte=latest_birthday
    ).exclude(id__in=sid_list)[:num]  # 懒加载, Django 会解析完整语句, 然后拼接成一条 SQL, 然后发给 MySQL 执行

    return users


def rcmd_users(uid):
    '''合并优先推荐和数据库中的数据,为用户推荐可以交友的对象'''
    user_from_q = set(rcmd_users_from_q(uid))
    remain = 25 - len(user_from_q)
    user_from_db = set(rcmd_users_from_db(uid, remain))
    print(user_from_q)
    print(user_from_db)
    return user_from_q | user_from_db


def like_someone(uid, sid):
    '''喜欢右滑了某人'''
    if not sid or uid == sid:
        raise err.SidErr('SID 错误')
    Swiper.swipe(uid, sid, 'like')
    # 强制从优先队列中删除sid
    name = keys.FIRST_RCMD_Q % uid
    rds.lrem(name, 1, sid)
    # 检查对方是否喜欢过自己，如果是则匹配成好友
    if Swiper.is_liked(sid, uid):
        Friend.make_friends(uid, sid)
        return True
    else:
        return False


def superlike_someone(uid, sid):
    '''超级喜欢上滑了某人'''
    if not sid or uid == sid:
        raise err.SidErr('SID 错误')
    Swiper.swipe(uid, sid, 'superlike')
    # 强制从优先队列中删除sid
    name = keys.FIRST_RCMD_Q % uid
    rds.lrem(name, 1, sid)
    # 检查对方是否喜欢过自己，如果是则匹配成好友
    is_liked = Swiper.is_liked(sid, uid)
    if is_liked == True:
        Friend.make_friends(uid, sid)
        return True
    elif is_liked is None:
        other_first_q = keys.FIRST_RCMD_Q % sid
        rds.rpush(other_first_q, uid) # 将 UID 添加到对方的优先推荐队列
        return False
    else:
        return False


def dislike_someone(uid, sid):
    '''不喜欢左滑了某人'''
    if not sid or uid == sid:
        raise err.SidErr('SID 错误')

    Swiper.swipe(uid, sid, 'dislike')
    # 强制从优先列表中删除
    my_first_q = keys.FIRST_RCMD_Q % sid
    rds.lrem(my_first_q, 1, sid)


def rewind_swipe(uid):
    '''
        反悔上一次的滑动

            Redis 中记录的数据: {
                'rewind_date': '2020-03-18',  # 反悔的日期
                'rewind_cnt': 0,              # 当天的反悔次数
            }
    '''
    # 从 Rides 中取出反悔数据
    rewind_key = keys.REWIND_K % uid
    rewind_data = rds.hgetall(rewind_key)
    rewind_date = rewind_data.get(b'rewind_date', '1970-01-01')
    rewind_cnt = rewind_data.get(b'rewind_cnt', 0)
    # 取出当前时间
    now = datetime.datetime.today()
    today = str(now.date())
    # 检查当天反悔次数是否超过3次
    if today == rewind_date:
        if rewind_cnt >= 3:
            raise err.RewindLimitErr('反悔次数上限')
    else:
        rewind_cnt = 0
    # 从数据库中获取最后一条记录，并判断是否为None
    last_swipe = Swiper.objects.filter(uid=uid).latest('stime')
    if last_swipe is None:
        raise err.NoneSwipe('当前没有反悔数据')
    # 检查时间是否超过五分钟
    if (now - last_swipe.stime) > datetime.timedelta(minutes=5):
        raise err.RewindTimeout('反悔超时')
    # 操作时开启事务
    with atomic():
        # 之前匹配的好友关系需要解除好友
        if last_swipe.stype in ['like', 'superlike']:
            Friend.break_off(uid, last_swipe.sid)
        # 删除滑动记录
        last_swipe.delete()
        # 之前是超级喜欢将ID从对方的优先队列中删除
        rds.lrem(keys.FIRST_RCMD_Q % last_swipe.sid, 0, uid)
        # 更新反悔数据
        rds.hmset(rewind_key, {'rewind_cnt': rewind_cnt + 1, 'rewind_date': today})


def who_is_like_me(uid):
    '''过滤出喜欢过我，但我还没有划过的人'''
    # 取出我以划过的sid列表
    sid_list = Swiper.objects.filter(uid=uid).values_list('sid', flat=True)
    # 取出uid列表
    uid_list = Swiper.objects.filter(sid=uid, stype__in=['like', 'superlike'])\
                                    .exclude(uid__in=sid_list)\
                                    .values_list('uid', flat=True)
    return User.objects.filter(id__in=uid_list)