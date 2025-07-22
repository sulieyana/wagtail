# 🚀 Wagtail + Keycloak Authentication Integration

This project integrates [Wagtail CMS](https://wagtail.org/) with [Keycloak](https://www.keycloak.org/) using OpenID Connect for authentication and secure session management.

> ✅ Users authenticate through Keycloak and are redirected back to Wagtail.  
> ✅ Wagtail admin session auto-invalidates if the Keycloak session is killed/expired.


[Wagtail Documentation](https://docs.wagtail.org/en/v7.0.1/) 
Topics, references, & how-tos

---

## 📦 Features

- ✅ Secure login via Keycloak using OpenID Connect (OIDC)
- ✅ Integrated with `mozilla-django-oidc`
- ✅ Access token stored in Django session
- ✅ Custom middleware to validate Keycloak session on every `/admin` request
- ✅ Auto logout in Wagtail if Keycloak session is killed

---

## ⚙️ Technology Stack

- **Python 3.10.11**
- **Django 5.2.4**
- **Wagtail 7.0.1**
- **mozilla-django-oidc**
- **Keycloak**
- **Requests (Python HTTP library)**




