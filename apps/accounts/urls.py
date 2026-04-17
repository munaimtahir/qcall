from django.urls import path

from apps.accounts import views

app_name = "accounts"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.RoleAwareLoginView.as_view(), name="login"),
    path("logout/", views.RoleAwareLogoutView.as_view(), name="logout"),
]
