import datetime

from user.models import User
from social.models import Swiper
from social.models import Friend


def rcmd_users(uid):
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
    ).exclude(id__in=sid_list)[:25]  # 懒加载, Django 会解析完整语句, 然后拼接成一条 SQL, 然后发给 MySQL 执行

    return users


def like_someone(uid, sid):
    '''喜欢右滑了某人'''
    if sid and uid != sid:
        Swiper.swipe(uid, sid, 'like')
        # 检查对方是否喜欢过自己，如果是则匹配成好友
        if Swiper.is_liked(sid, uid):
            Friend.make_friends(uid, sid)
            return True
        else:
            return False
    else:
        return 'ID错误'

