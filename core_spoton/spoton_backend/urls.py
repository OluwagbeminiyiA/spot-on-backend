from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core_spoton.api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path(
        "logged-in/",
        login_required(TemplateView.as_view(template_name="registration/../../templates/registration/logged_in.html")),
        name="logged_in",
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
