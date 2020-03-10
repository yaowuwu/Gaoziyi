from django.http import JsonResponse


def get_vcode(request):
    '''获取短信验证码'''
    return JsonResponse({})


def submit_vcode(request):
    '''通过验证码登陆，注册'''
    return JsonResponse({})


def show_profile(request):
    '''查看个人交友资料'''
    return JsonResponse({})


def modify_profile(request):
    '''修改个人资料及交友资料'''
    return JsonResponse({})


def upload_avatar(request):
    '''头像上传'''
    return JsonResponse({})