from django.urls import path
from . import views


urlpatterns = [
    path("", views.home_view, name='home_view'),
    path("check_auth", views.check_auth_view, name='check_auth_view'),
    path("logout", views.logout_view, name='logout_view'),
]
