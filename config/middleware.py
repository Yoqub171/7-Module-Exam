import datetime
from django.utils import timezone
from django.contrib.auth import logout

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        print(f"Request method {request.method}, Request Path: {request.path}")
        response = self.get_response(request)
        return response



class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            now = timezone.now()
            last_activity = request.session.get('last_activity')

            if last_activity:
                elapsed_time = now - datetime.datetime.fromisoformat(last_activity)
                if elapsed_time.total_seconds() > 3600:
                    logout(request)
                    print(f"[AutoLogout] User was automatically logged out ({request.user.username})")
            request.session['last_activity'] = now.isoformat()

        response = self.get_response(request)
        return response
