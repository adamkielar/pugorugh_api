from django.urls import path, register_converter
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from . import views
from . import converters


register_converter(converters.UserDogStatusConverter, "dogstatus")
# API endpoints
urlpatterns = format_suffix_patterns(
    [
        path("api/user/login/", obtain_auth_token, name="login-user"),
        path("api/user/", views.UserRegisterView.as_view(), name="register-user"),
        path(
            "api/user/preferences/",
            views.UserPreferencesView.as_view(),
            name="preferences",
        ),
        path("api/dog/", views.DogListView.as_view(), name="dog-list"),
        path(
            "api/dog/<int:pk>/<dogstatus:status>",
            views.UserDogStatusUpdateView.as_view(),
            name="dog-update",
        ),
        path(
            "api/dog/<int:pk>/<dogstatus:status>/next/",
            views.DogRetrieve.as_view(),
            name="dog-retrieve",
        ),
        path("api/dog/add", views.CreateDogView.as_view(), name="create-dog"),
        path(
            "api/dog<int:pk>/delete", views.DeleteDogView.as_view(), name="delete-dog"
        ),
        path(
            "favicon.ico",
            RedirectView.as_view(url="/static/icons/favicon.ico", permanent=True),
        ),
        path("", TemplateView.as_view(template_name="index.html")),
    ]
)
