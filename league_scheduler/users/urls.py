from django.urls import path
from users import views

urlpatterns = [
    path(r'authorize', views.authorize),
    path(r'login', views.login, name = "login"),
    path(r'logout', views.logout_view, name = "logout"),
]
