from django.contrib import admin, messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect, render
from django.urls import path, reverse

from .forms import ProfileAdminForm, ProfilePasswordForm
from .models import Profile, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_superuser", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    def has_module_permission(self, request):
        return False


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "updated_at")

    def has_module_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        return False


def profile_admin_view(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect("admin:login")

    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "profile":
            form = ProfileAdminForm(
                request.POST,
                request.FILES,
                instance=profile,
                user=request.user,
            )
            password_form = ProfilePasswordForm(user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect("admin:core_profile")
            messages.error(request, "Please correct the profile errors below.")

        elif action == "password":
            password_form = ProfilePasswordForm(user=request.user, data=request.POST)
            form = ProfileAdminForm(instance=profile, user=request.user)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully.")
                return redirect("admin:core_profile")
            messages.error(request, "Please correct the password errors below.")
        else:
            form = ProfileAdminForm(instance=profile, user=request.user)
            password_form = ProfilePasswordForm(user=request.user)
    else:
        form = ProfileAdminForm(instance=profile, user=request.user)
        password_form = ProfilePasswordForm(user=request.user)

    context = {
        **admin.site.each_context(request),
        "title": "Profile",
        "form": form,
        "password_form": password_form,
        "profile": profile,
        "opts": Profile._meta,
        "app_label": Profile._meta.app_label,
    }
    return render(request, "admin/core/profile.html", context)


_original_get_urls = admin.site.get_urls


def _custom_admin_urls():
    custom_urls = [
        path(
            "profile/",
            admin.site.admin_view(profile_admin_view),
            name="core_profile",
        ),
    ]
    return custom_urls + _original_get_urls()


admin.site.get_urls = _custom_admin_urls
admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Dashboard"
