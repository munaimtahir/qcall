from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from apps.accounts.models import UserRole


class RoleAwareLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.role == UserRole.ADMIN:
            return reverse_lazy("settings_app:settings-home")
        if user.role == UserRole.DOCTOR:
            return reverse_lazy("doctor-dashboard")
        return reverse_lazy("reception-dashboard")


class RoleAwareLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


def home(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    if request.user.is_superuser or request.user.role == UserRole.ADMIN:
        return redirect("settings_app:settings-home")
    if request.user.role == UserRole.DOCTOR:
        return redirect("doctor-dashboard")
    return redirect("reception-dashboard")
