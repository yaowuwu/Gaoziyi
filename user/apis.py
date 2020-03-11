from django.core.cache import cache
from django.views.decorators.http import require_http_methods

from user import logics
from libs.http import render_json
from common import err
from common import keys
from user.models import User
from user.models import Profile


def get_vcode(request):
    '''获取短信验证码'''
    phonenum = request.GET.get('phonenum')
    is_successed = logics.send_vcode(phonenum)
    if is_successed:
        return render_json()
    else:
        return render_json(code=err.VCODE_SEND_ERR)


# @require_http_methods(['POST'])
def submit_vcode(request):
    ''' 通过验证码登陆，注册 '''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    # 从缓存中获取验证码
    key = keys.VCODE_K % phonenum
    cache_vcode = cache.get(key)
    if vcode and vcode == cache_vcode:
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)
        # 记录用户的登陆信息
        request.session['uid'] = user.id
        return render_json(user.to_dict())
    else:
        print('aaaaaaaaaaaaaaaaaaa')
        return render_json(code=err.VCODE_ERR)


def show_profile(request):
    '''查看个人交友资料'''
    user = User.objects.get(id=request.uid)
    if user:
        return render_json(user.to_dict())
    else:
        return True


def modify_profile(request):
    '''修改个人资料及交友资料'''
    user = User.objects.get(id=request.uid)
    user.nickname = request.POST.get('nickname')
    user.location = request.POST.get('location')
    user.gender = request.POST.get('gender')
    user.birthday = request.POST.get('birthday')
    user.save()
    profile = Profile()
    profile.uid = request.uid
    profile.dating_location = request.POST.get('dating_location')
    profile.min_distance = request.POST.get('min_distance')
    profile.max_distance = request.POST.get('max_distance')
    profile.min_dating_age = request.POST.get('min_dating_age')
    profile.max_dating_age = request.POST.get('max_dating_age')
    profile.dating_sex = request.POST.get('dating_sex')
    profile.vibration = request.POST.get('vibration')
    profile.only_matched = request.POST.get('only_matched')
    profile.auto_play = request.POST.get('auto_play')
    profile.save()
    return render_json()


def upload_avatar(request):
    '''头像上传'''
    return render_json({})