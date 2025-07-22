from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from django.contrib.auth.models import User

class KeycloakOIDCBackend(OIDCAuthenticationBackend):
    # def filter_users_by_claims(self, claims):
       
    #     """
    #     Store id_token and request before user is created or updated.
    #     This method is reliably called first in the pipeline.
    #     """
    #     request = self._request  # This will be set via authenticate()
    #     id_token = getattr(request, 'session', {}).get('oidc_id_token')

    #     print("✅ filter_users_by_claims called with claims:", id_token,self, claims)

    #     if not id_token:
    #         # This grabs the id_token from self (OIDCAuthenticationBackend stores it)
    #         id_token = getattr(self, 'id_token', None)
    #         if id_token:
    #             request.session['oidc_id_token'] = id_token
    #             print("✅ Stored id_token in session from filter_users_by_claims")

    #     # Call parent logic to get user
    #     return super().filter_users_by_claims(claims)

    def authenticate(self, request, **kwargs):
        user = super().authenticate(request, **kwargs)

        # Save id_token in session for logout
        if user and request and 'id_token' in kwargs:
            request.session['oidc_id_token'] = kwargs['id_token']
            print("✅ Saved id_token in session for logout")

        return user

    def create_user(self, claims):
        print("✅ Creating user with claims:", claims)
        username = claims.get("preferred_username") or claims.get("email") or claims.get("sub")
        user = User.objects.create_user(username=username)
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.email = claims.get("email", "")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

    def update_user(self, user, claims):
        print("✅ Updating user with claims:", claims)
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.email = claims.get("email", "")
        user.is_staff = True
        user.save()
        return user
