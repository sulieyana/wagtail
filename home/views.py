# home/views.py
print("🔥 CustomOIDCCallbackView LOADED")
from django.contrib.auth import logout as django_logout
from django.shortcuts import redirect
from django.conf import settings
from django.shortcuts import resolve_url

# from mozilla_django_oidc.views import OIDCAuthenticationCallbackView, OIDCAuthenticationRequestView
from mozilla_django_oidc.views import OIDCAuthenticationCallbackView
from django.utils.http import urlencode
import jwt

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import logout
from django.middleware.csrf import get_token


class CustomOIDCCallbackView(OIDCAuthenticationCallbackView):
    def get(self, request):
        response = super().get(request)
        
        # Extract access token
        access_token = request.session.get("oidc_access_token")
        if access_token:
            try:
                # Decode without verification, assuming it's a JWT
                decoded = jwt.decode(access_token, options={"verify_signature": False})
                exp = decoded.get("exp")
                if exp:
                    request.session["oidc_access_token_exp"] = exp
                    print("✅ Stored token expiration:", exp)
            except Exception as e:
                print("❌ Failed to decode token:", str(e))
        
        return response

def wagtail_admin_redirect_to_oidc(request):
    return redirect(settings.LOGIN_URL)  

def force_token_expired(request):
    request.session["oidc_access_token_exp"] = 0  # Set to past timestamp
    return HttpResponse("✅ Simulated token expiry")

# class CustomOIDCCallbackView(OIDCAuthenticationCallbackView):
#     def get(self, request):
#         # response = super().get(request)
#         # next_url = request.session.pop('oidc_login_next', '/')
#         # print("🔗 Redirecting to:", next_url)
#         # return redirect(next_url)
    
#         redirect_to = request.GET.get("next") or "/admin/"
#         return redirect(resolve_url(redirect_to))

    
# class CustomOIDCLoginView(OIDCAuthenticationRequestView):
#     def get(self, request):
#         next_url = request.GET.get('next', '/')
#         request.session['oidc_login_next'] = next_url  # store it for the callback

#         print("🔗 Redirecting to authenticate:", next_url)
#         return super().get(request)

# not used, but kept for reference
def custom_logout(request):
    id_token = request.session.get("oidc_id_token")
    print("🧪 id_token from session:", id_token)

    # Logout locally
    django_logout(request)

    if not id_token:
        print("❌ No id_token in session, skipping Keycloak logout.")
        return redirect("/")

    logout_url = (
        f"{settings.OIDC_OP_LOGOUT_ENDPOINT}"
        f"?id_token_hint={id_token}"
        f"&post_logout_redirect_uri={request.build_absolute_uri('/')}"
    )
    print("✅ Redirecting to Keycloak logout URL:", logout_url)
    return redirect(logout_url)


def custom_admin_logout(request):
    id_token = request.session.get("oidc_id_token")
    print("🧪 id_token from session:", id_token)
    django_logout(request)  # Clear local Django session

    if not id_token:
        print("❌ No id_token found. Redirecting to home.")
        return redirect("/")
        

    logout_url = (
        f"{settings.OIDC_OP_LOGOUT_ENDPOINT}"
        f"?id_token_hint={id_token}"
        f"&post_logout_redirect_uri={request.build_absolute_uri('/admin')}"
    )

    print("✅ Redirecting to Keycloak logout:", logout_url)
    return redirect(logout_url)

@csrf_exempt
def remote_logout(request):
    if request.method == "POST":
        logout(request)
        request.session.flush()
        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Invalid method"}, status=400)



