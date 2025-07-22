# middleware/token_expiry.py
import time
from django.shortcuts import redirect
from django.contrib.auth import logout

class TokenExpiryMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        print("🔍 request:", request)

        # Only check authenticated users accessing admin
        if hasattr(request, "user") and request.user.is_authenticated and path.startswith("/admin"):
            exp = request.session.get("oidc_access_token_exp")
            now = int(time.time())
            print("🔍 exp value:", exp)
            print("🔍 current time:", now)
            if exp is None or now >= int(exp):
               
                logout(request)
                request.session.flush()
                return redirect("/oidc/authenticate/?next=/admin/")

        return self.get_response(request)

    # def __init__(self, get_response):
    #     self.get_response = get_response

    # def __call__(self, request):
    #     if request.path.startswith("/admin/"):
    #         exp = request.session.get("oidc_access_token_exp")
    #         now = int(time.time())
    #         print("✅ TokenExpiryMiddleware checking token expiry", exp)

    #         print("🔍 exp value:", exp)
    #         print("🔍 current time:", now)

    #         if exp is not None:
    #             try:
    #                 if now >= int(exp):
    #                     print("⛔ Token expired, logging out")
    #                     logout(request)
    #                     return redirect("/oidc/authenticate/?next=/admin/")
    #             except (TypeError, ValueError):
    #                 logout(request)
    #                 return redirect("/oidc/authenticate/?next=/admin/")

    #     return self.get_response(request)
    

        #     if exp is not None and now >= int(exp):
        #         print("⚠️ Token expired. Logging out.")
        #         logout(request)
        #         return redirect("/oidc/authenticate/?next=/admin/")
        #     else:
        #         print("✅ Token still valid.")


        #     # if exp and now >= exp:

        #     #     print("⛔ Token expired, logging out")
        #     #     logout(request)
        #     #     return redirect("/oidc/authenticate/?next=/admin/")

        # return self.get_response(request)
    


    # if request.path.startswith("/admin/"):
    # exp = request.session.get("oidc_access_token_exp")
    # if exp and time.time() >= exp:
    #     logout(request)
    #     return redirect("/oidc/authenticate/?next=/admin/")
