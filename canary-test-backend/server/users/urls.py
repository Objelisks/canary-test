from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("select_repo", views.select_repo, name="select_repo"),
    path("authorize", views.authorize, name="callback"),
    path("webhook", views.webhook, name="webhook"),
]