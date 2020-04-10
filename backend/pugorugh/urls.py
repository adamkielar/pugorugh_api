from django.urls import path, re_path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from . import views


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
        path("api/dog/", views.DogListAddView.as_view(), name="dog-list"),
        re_path(
            r"^api/dog/(?P<pk>-?\d+)/(?P<status>liked|disliked|undecided)/$",
            views.UserDogStatusUpdateView.as_view(),
            name="dog-update",
        ),
        re_path(
            r"^api/dog/(?P<pk>-?\d+)/(?P<status>liked|disliked|undecided)/next/$",
            views.DogRetrieve.as_view(),
            name="dog-retrieve",
        ),
        path("api/dog/add", views.DogListAddView.as_view(), name="create-dog"),
        path(
            "api/dog/<int:pk>/delete", views.DeleteDogView.as_view(), name="delete-dog"
        ),
        path(
            "favicon.ico",
            RedirectView.as_view(url="/static/icons/favicon.ico", permanent=True),
        ),
        path("", TemplateView.as_view(template_name="index.html")),
    ]
)
