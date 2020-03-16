import datetime

from django.core.cache import cache
from libs.http import render_json
from user.models import User
from social.models import Swiper
from user.models import Profile
from social import logics


def rcmd_user(request):
    '''获取推荐列表'''
    users = logics.rcmd_users(request.uid)
    result = [user.to_dict() for user in users]
    return render_json(result)


def like(request):
    '''喜欢右滑'''
    sid = int(request.POST.get('sid'))
    is_matched = logics.like_someone(request.uid, sid)
    return render_json({'is_matched': is_matched})
