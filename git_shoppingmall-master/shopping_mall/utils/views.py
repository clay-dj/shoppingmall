from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.http import JsonResponse


class LoginRequiredJSONMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        return JsonResponse({'code': 400, 'errmsg': '没有登录'})
from fdfs_client.client import Fdfs_client

