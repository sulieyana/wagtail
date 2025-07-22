print("✅ wagtail_hooks.py loaded")  # top-level test

from django.conf import settings
from django.shortcuts import redirect

from django.templatetags.static import static
from django.utils.html import format_html

from wagtail import hooks

@hooks.register('before_serve_admin')
def require_oidc_login(request):
    print("✅ Hook triggered in home /admin")
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)

@hooks.register("insert_global_admin_css")
def global_admin_css():
    # This injects a custom script into the Wagtail admin
    return format_html('<script src="{}"></script>', static("js/custom-admin.js"))
