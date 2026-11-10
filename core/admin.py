from django import forms
from django.contrib import admin, messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.html import format_html

from core.validators import media_type_from_filename

from .forms import ProfileAdminForm, ProfilePasswordForm
from .models import (
    ContactMessage,
    EducationItem,
    HeroMetric,
    Profile,
    Project,
    ProjectImage,
    Service,
    ServiceDeliverable,
    ServiceFAQ,
    ServiceMedia,
    ServiceProcessStep,
    ServiceUseCase,
    SocialLink,
    TechnicalSkill,
    User,
)


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


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(TechnicalSkill)
class TechnicalSkillAdmin(admin.ModelAdmin):
    list_display = ("skill_id", "title", "mastery", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "year", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("category", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order",)
    inlines = [ProjectImageInline]


def _media_preview(file_field, media_type="", poster_url=""):
    if not file_field:
        return "—"
    url = file_field.url
    is_video = media_type == "video" or url.lower().endswith((".mp4", ".webm", ".mov"))
    if is_video:
        if poster_url:
            return format_html(
                '<video src="{}" poster="{}" style="max-height:80px;max-width:140px;" muted></video>',
                url,
                poster_url,
            )
        return format_html(
            '<video src="{}" style="max-height:80px;max-width:140px;" muted></video>',
            url,
        )
    return format_html(
        '<img src="{}" alt="" style="max-height:80px;max-width:140px;'
        'object-fit:cover;border-radius:8px;" />',
        url,
    )


class OrderedInline(admin.TabularInline):
    extra = 1
    ordering = ("order",)


class ServiceDeliverableInline(OrderedInline):
    model = ServiceDeliverable
    fields = ("order", "title", "description")


class ServiceProcessStepInline(OrderedInline):
    model = ServiceProcessStep
    fields = ("order", "title", "description")


class ServiceUseCaseInline(OrderedInline):
    model = ServiceUseCase
    fields = ("order", "title", "description")


class ServiceFAQInline(OrderedInline):
    model = ServiceFAQ
    fields = ("order", "question", "answer")


class ServiceMediaForm(forms.ModelForm):
    class Meta:
        model = ServiceMedia
        fields = (
            "order",
            "media_type",
            "file",
            "poster",
            "caption",
            "alt_text",
            "featured",
        )

    def clean(self):
        cleaned = super().clean()
        uploaded = cleaned.get("file")
        if uploaded and not cleaned.get("media_type"):
            cleaned["media_type"] = media_type_from_filename(uploaded.name)
        return cleaned


class ServiceMediaInline(OrderedInline):
    model = ServiceMedia
    form = ServiceMediaForm
    fields = (
        "order",
        "media_type",
        "file",
        "file_preview",
        "poster",
        "poster_preview",
        "caption",
        "alt_text",
        "featured",
    )
    readonly_fields = ("file_preview", "poster_preview")

    @admin.display(description="File preview")
    def file_preview(self, obj):
        poster_url = obj.poster.url if obj.pk and obj.poster else ""
        return _media_preview(obj.file if obj.pk else None, obj.media_type, poster_url)

    @admin.display(description="Poster preview")
    def poster_preview(self, obj):
        return _media_preview(obj.poster if obj.pk else None, "image")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("cover_preview", "title", "slug", "order", "is_published")
    list_display_links = ("cover_preview", "title")
    list_editable = ("order", "is_published")
    list_filter = ("is_published",)
    search_fields = ("title", "slug", "tagline", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order",)
    readonly_fields = ("cover_preview_large", "updated_at")
    inlines = [
        ServiceDeliverableInline,
        ServiceProcessStepInline,
        ServiceUseCaseInline,
        ServiceFAQInline,
        ServiceMediaInline,
    ]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "description":
            kwargs["widget"] = forms.Textarea(attrs={"rows": 14, "cols": 80})
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    fieldsets = (
        (
            "Listing",
            {
                "fields": (
                    "title",
                    "slug",
                    "tagline",
                    "icon",
                    "order",
                    "is_published",
                )
            },
        ),
        (
            "Copy",
            {"fields": ("description", "cta_text", "tech_stack")},
        ),
        (
            "Cover",
            {"fields": ("cover_image", "cover_preview_large")},
        ),
        (
            "Meta",
            {"fields": ("updated_at",)},
        ),
    )

    @admin.display(description="Cover")
    def cover_preview(self, obj):
        return _media_preview(obj.cover_image, "image")

    @admin.display(description="Cover preview")
    def cover_preview_large(self, obj):
        if not obj.cover_image:
            return "—"
        return format_html(
            '<img src="{}" alt="" style="max-height:180px;max-width:320px;'
            'object-fit:cover;border-radius:12px;" />',
            obj.cover_image.url,
        )


@admin.register(EducationItem)
class EducationItemAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "period", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "label", "url", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)


@admin.register(HeroMetric)
class HeroMetricAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "color", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    list_filter = ("created_at",)
    readonly_fields = ("name", "email", "subject", "message", "created_at")
    ordering = ("-created_at",)


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
