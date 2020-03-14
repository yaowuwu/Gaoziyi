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
            return render_json(code=err.LOGIN_REQUIRED)
        else:
            request.uid = uid