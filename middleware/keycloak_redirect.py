print("✅ keycloak_redirect.py loaded")  # top-level test

from django.shortcuts import redirect
from django.conf import settings

class KeycloakAdminRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin') and not request.user.is_authenticated:
            print("✅ Redirecting unauthenticated /admin/ to Keycloak")
            return redirect(settings.LOGIN_URL)
        return self.get_response(request)
