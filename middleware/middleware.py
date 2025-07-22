import time
from django.shortcuts import redirect
from django.contrib.auth import logout

class TokenExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check for logged-in users

        if request.user.is_authenticated:
            exp = request.session.get("oidc_access_token_exp")
            now = int(time.time())
            print(f"🔐 exp: {exp} | now: {now}")
            if exp is not None and now >= int(exp):
                print("⛔ Token expired — logging out")
                logout(request)
                return redirect("/")
                return redirect("/oidc/authenticate/?next=/admin/")
    

        # if request.user.is_authenticated:
        #     exp = request.session.get("oidc_access_token_exp")
        #     now = int(time.time())

        #     # Debug print (optional)
        #     print(f"🔐 exp: {exp} | now: {now}")

        #     if int(exp) and int(now) >= int(exp):
        #         print("⛔ Token expired — logging out")
        #         logout(request)
        #         return redirect("/oidc/authenticate/?next=/admin/")  # Or your login URL

        # return self.get_response(request)
