from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path

from core.media_views import serve_local_media
from core.project_views import (
    admin_projects_detail_view,
    admin_projects_list_view,
    public_project_detail,
    public_projects_list,
)
from core.views import (
    admin_password_view,
    admin_profile_view,
    contact_submit,
    csrf_view,
    login_view,
    logout_view,
    me_view,
    public_education,
    public_hero_metrics,
    public_profile,
    public_skills,
    public_social_links,
)

urlpatterns = [
    # Public APIs
    path("api/profile/public/", public_profile, name="public_profile"),
    path("api/skills/", public_skills, name="public_skills"),
    path("api/education/", public_education, name="public_education"),
    path("api/hero-metrics/", public_hero_metrics, name="public_hero_metrics"),
    path("api/social-links/", public_social_links, name="public_social_links"),
    path("api/projects/", public_projects_list, name="public_projects_list"),
    path("api/projects/<slug:slug>/", public_project_detail, name="public_project_detail"),
    path("api/contact/", contact_submit, name="contact_submit"),
    # Auth
    path("api/auth/csrf/", csrf_view, name="api_csrf"),
    path("api/auth/login/", login_view, name="api_login"),
    path("api/auth/logout/", logout_view, name="api_logout"),
    path("api/auth/me/", me_view, name="api_me"),
    # Admin APIs
    path("api/admin/profile/", admin_profile_view, name="admin_profile"),
    path("api/admin/profile/password/", admin_password_view, name="admin_password"),
    path("api/admin/projects/", admin_projects_list_view, name="admin_projects_list"),
    path("api/admin/projects/<int:pk>/", admin_projects_detail_view, name="admin_projects_detail"),
    # Django admin
    path("django-admin/", admin.site.urls),
]

if not settings.USE_REMOTE_MEDIA:
    urlpatterns += [
        path("api/media/<path:path>", serve_local_media, name="serve_local_media"),
        re_path(r"^media/(?P<path>.*)$", serve_local_media, name="serve_legacy_media"),
    ]
