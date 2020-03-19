from common import err
from user.models import User


def perm_require(perm_name):
    def wrapper1(view_func):
        def wrapper2(request, *args, **kwargs):
            user = User.objects.get(id=request.uid)
            # 检查用户的VIP所具有的权限
            if user.vip.has_perm(perm_name):
                response = view_func(request, *args, **kwargs)
                return response
            else:
                raise err.PermRequired('当前用户不具有此权限')
        return wrapper2
    return wrapper1