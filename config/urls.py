from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from core.content_views import (
    admin_persona_view,
    admin_philosophy_detail_view,
    admin_philosophy_list_view,
    admin_skills_detail_view,
    admin_skills_list_view,
    public_home_content,
)
from core.project_views import (
    admin_projects_detail_view,
    admin_projects_list_view,
    public_project_detail,
    public_projects_list,
)
from core.views import (
    admin_password_view,
    admin_profile_view,
    csrf_view,
    login_view,
    logout_view,
    me_view,
    public_profile,
)

urlpatterns = [
    path("api/profile/public/", public_profile, name="public_profile"),
    path("api/home/content/", public_home_content, name="public_home_content"),
    path("api/auth/csrf/", csrf_view, name="api_csrf"),
    path("api/auth/login/", login_view, name="api_login"),
    path("api/auth/logout/", logout_view, name="api_logout"),
    path("api/auth/me/", me_view, name="api_me"),
    path("api/admin/profile/", admin_profile_view, name="admin_profile"),
    path("api/admin/profile/password/", admin_password_view, name="admin_password"),
    path("api/admin/persona/", admin_persona_view, name="admin_persona"),
    path("api/admin/philosophy/", admin_philosophy_list_view, name="admin_philosophy_list"),
    path(
        "api/admin/philosophy/<int:pk>/",
        admin_philosophy_detail_view,
        name="admin_philosophy_detail",
    ),
    path("api/admin/skills/", admin_skills_list_view, name="admin_skills_list"),
    path("api/admin/skills/<int:pk>/", admin_skills_detail_view, name="admin_skills_detail"),
    path("api/projects/", public_projects_list, name="public_projects_list"),
    path("api/projects/<slug:slug>/", public_project_detail, name="public_project_detail"),
    path("api/admin/projects/", admin_projects_list_view, name="admin_projects_list"),
    path(
        "api/admin/projects/<int:pk>/",
        admin_projects_detail_view,
        name="admin_projects_detail",
    ),
    path("django-admin/", admin.site.urls),
]

if settings.DEBUG and not settings.USE_CLOUDINARY:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
