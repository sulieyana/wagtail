from django.conf import settings
from django.urls import include, path
from django.contrib import admin


from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

from home.views import custom_admin_logout, custom_logout, force_token_expired, remote_logout,wagtail_admin_redirect_to_oidc


# from django.contrib.auth.views import LogoutView
# from django.shortcuts import redirect
# import urllib.parse

from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter

api_router = WagtailAPIRouter('wagtailapi')
api_router.register_endpoint('pages', PagesAPIViewSet)


# Example for DRF + Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path

from home.views import CustomOIDCCallbackView

from django.urls import URLResolver, URLPattern

# from home.views import CustomOIDCCallbackView, CustomOIDCLoginView

schema_view = get_schema_view(
   openapi.Info(
      title="Wagtail API",
      default_version='v1',
      description="Wagtail Headless API documentation",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


# def keycloak_logout(request):
#     id_token = request.session.get('oidc_id_token', '')
#     django_logout(request)

#     post_logout_redirect_uri = request.build_absolute_uri('/')  # Change if needed
#     params = {
#         'post_logout_redirect_uri': post_logout_redirect_uri,
#     }

#     if id_token:
#         params['id_token_hint'] = id_token

#     logout_url = f"{settings.OIDC_OP_LOGOUT_ENDPOINT}?{urllib.parse.urlencode(params)}"
#     return redirect(logout_url)


urlpatterns = [
   
    # path("django-admin/", admin.site.urls),
    # path('oidc/authenticate/', CustomOIDCLoginView.as_view(), name='oidc_authentication_init'),
    # path('oidc/callback/', CustomOIDCCallbackView.as_view(), name='oidc_callback'), 
    
    path("health/", include("health_check.urls")),   # → /health/
    path("admin/login/", wagtail_admin_redirect_to_oidc),
    
    # All other routes
    path("admin/", include(wagtailadmin_urls)),

    path("oidc/callback/", CustomOIDCCallbackView.as_view(), name="oidc_callback"),
    path('admin/logout/', custom_admin_logout, name='wagtailadmin_logout'),  
    # path("admin/", include(wagtailadmin_urls)),
    path("logout/", custom_logout, name="custom_logout"),
    path('oidc/', include('mozilla_django_oidc.urls')), 
   
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path("force-expiry/", force_token_expired),
    path('api/remote-logout/', remote_logout, name='remote-logout')
    #  path("logout/", keycloak_logout, name="logout"),
    
]

urlpatterns += [
    path('api/v2/', api_router.urls),
]

urlpatterns += [
    path('api-docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]

if settings.URL_PREFIX:
    urlpatterns = [path(f'{settings.URL_PREFIX}/', include(urlpatterns))]

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Serve static and media files from development server
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



