import logging

from libs.http import render_json
from social import logics
from social.models import Friend
from user.models import User
from vip.logics import perm_require

inflog = logging.getLogger('inf')


def rcmd_user(request):
    '''获取推荐列表'''
    users = logics.rcmd_users(request.uid)
    result = [user.to_dict() for user in users]
    return render_json(result)


def like(request):
    '''喜欢右滑'''
    sid = int(request.POST.get('sid', 0))
    is_matched = logics.like_someone(request.uid, sid)
    inflog.debug(f'User({request.uid}) like User({sid}): {is_matched}')
    return render_json({'is_matched': is_matched})


@perm_require('superlike')
def superlike(request):
    '''超级喜欢(上滑)'''
    sid = int(request.POST.get('sid', 0))
    is_matched = logics.superlike_someone(request.uid, sid)
    inflog.debug(f'User({request.uid}) superlike User({sid}): {is_matched}')
    return render_json({'is_matched': is_matched})


def dislike(request):
    '''不喜欢(左滑)'''
    sid = int(request.POST.get('sid', 0))
    logics.dislike_someone(request.uid, sid)
    inflog.debug(f'User({request.uid}) dislike User({sid})')
    return render_json()


@perm_require('rewind')
def rewind(request):
    '''反悔最后一次的滑动

    - 每天允许反悔 3 次
    - 反悔的记录只能是五分钟之内的
    '''
    logics.rewind_swipe(request.uid)
    return render_json()


@perm_require('who_liked_me')
def show_users_liked_me(request):
    '''查看都有谁喜欢过我的人

    - 我还没有滑过对方
    - 对方右滑或者上滑过自己
    '''
    users = logics.who_is_like_me(request.uid)
    result = [user.to_dict() for user in users]
    return render_json(result)


def friends(request):
    '''好友列表'''
    fid_list = Friend.friend_id_list(request.uid)
    users = User.objects.filter(id__in=fid_list)
    result = [user.to_dict() for user in users]
    return render_json(result)


def hot_rank(request):
    '''
        查看全服人气热度前 50 的用户

        Return:
            rank_data = {
                '1': {'score': 81623, 'nickname': xxx, 'avatar': xxxx, 'id': xx, 'gender': xx},
                '2': {'score': 73223, 'nickname': xxx, 'avatar': xxxx, 'id': xx, 'gender': xx},
                '3': {'score': 63529, 'nickname': xxx, 'avatar': xxxx, 'id': xx, 'gender': xx},
            }
    '''
    rank_data = logics.get_top_n(50)
    return render_json(rank_data)