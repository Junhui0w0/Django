# myapp/middleware.py
from django.http import HttpResponseForbidden

class BlockScrapersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # 차단하고 싶은 유저 에이전트 키워드 추가
        self.bad_user_agents = ['scanner', 'python', 'googlebot'] 

    def __call__(self, request):
        user_agent = request.headers.get('User-Agent', '').lower()
        for agent in self.bad_user_agents:
            if agent in user_agent:
                return HttpResponseForbidden('접근이 허용되지 않습니다.')

        response = self.get_response(request)
        return response