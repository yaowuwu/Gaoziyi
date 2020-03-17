from django.utils.deprecation import MiddlewareMixin

from libs.http import render_json
from common import err


class AuthMiddleware(MiddlewareMixin):
    white_list = [
        '/api/user/get_vcode',
        '/api/user/submit_vcode',
    ]

    def process_request(self, request):
        if request.path in self.white_list:
            return
        uid = request.session.get('uid')
        if not uid:
            return render_json(code=err.LogicError.code)
        else:
            request.uid = uid


class StatusCodeMiddleware(MiddlewareMixin):
    '''状态码处理中间件'''
    def process_exception(self, request, exception):
        if isinstance(exception, err.LogicError):
            return render_json(exception.data, exception.code)