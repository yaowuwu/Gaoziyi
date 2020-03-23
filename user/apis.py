import logging

from django.core.cache import cache
from django.views.decorators.http import require_http_methods

from user import logics
from libs.http import render_json
from common import err
from common import keys
from user.models import User
from user.models import Profile
from user import forms
from libs.cache import rds

inflog = logging.getLogger('inf')


def get_vcode(request):
    '''获取短信验证码'''
    phonenum = request.GET.get('phonenum')
    is_successed = logics.send_vcode(phonenum)
    if is_successed:
        return render_json()
    else:
        raise err.VcodeSendErr('验证码发送失败')


@require_http_methods(['POST'])
def submit_vcode(request):
    ''' 通过验证码登陆，注册 '''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    # 从缓存中获取验证码
    key = keys.VCODE_K % phonenum
    cache_vcode = cache.get(key)
    print(cache_vcode)
    print(vcode)
    if vcode and vcode == cache_vcode:
        try:
            user = User.objects.get(phonenum=phonenum)
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)
        # 记录用户的登陆信息
        request.session['uid'] = user.id
        return render_json(user.to_dict())
    else:
        raise err.VcodeErr('验证码错误')


def show_profile(request):
    ''' 查看个人交友资料 '''
    key = keys.USER_PROFILE_K % request.uid

    # 先从缓存中获取数据
    # result = rds.get(key, {})
    # inflog.debug('从缓存中获取:%s' % result)
    # 如果result为空值，则从数据库中获取数据
    # if not result:
    result = {}
    user = User.objects.get(id=request.uid)  # 从数据库中获取user
    result.update(user.to_dict())
    result.update(user.profile.to_dict())    # 从数据库中获取profile
        # inflog.debug('从数据库中获取: %s' % result)
        # rds.set(key, result)                     # 将结果保存到缓存中
        # inflog.debug('将数据写入缓存')
    return render_json(result)


def modify_profile(request):
    '''修改个人资料及交友资料'''
    # 定义两个Form表单
    user_form = forms.UserForm(request.POST)
    profile_form = forms.ProfileForm(request.POST)
    # 检查user_form 和 profile_form
    if not user_form.is_valid() or not profile_form.is_valid():
        errors = {}
        errors.update(user_form.errors)
        errors.update(profile_form.errors)

        raise err.ProfileErr(errors)

    # 更新user数据
    User.objects.filter(id=request.uid).update(**user_form.cleaned_data)
    # 更新profile数据
    Profile.objects.update_or_create(id=request.uid, defaults=profile_form.cleaned_data)
    key = keys.USER_PROFILE_K % request.uid
    rds.delete(key)
    return render_json()


def upload_avatar(request):
    '''个人照片上传'''
    avatar = request.FILES.get('avatar')  # 获取上传的文件对象
    logics.handle_avatar.delay(request.uid, avatar)
    return render_json()