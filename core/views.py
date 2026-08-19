from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import get_user_model
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from core.forms import ProfilePasswordForm
from core.models import (
    ContactMessage,
    EducationItem,
    HeroMetric,
    Profile,
    SocialLink,
    TechnicalSkill,
)
from core.permissions import IsSuperUser
from core.project_serializers import _absolute_media_url

User = get_user_model()


def _build_profile_payload(user, request):
    profile, _ = Profile.objects.get_or_create(user=user)
    picture_url = None
    if profile.profile_picture:
        picture_url = _absolute_media_url(request, profile.profile_picture)

    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": user.full_name,
        "email": user.email,
        "profile_picture": picture_url,
        "about_description": profile.about_description,
        "job_title": profile.job_title,
        "hero_heading": profile.hero_heading,
        "hero_description": profile.hero_description,
        "resume_summary": profile.resume_summary,
        "status_text": profile.status_text,
        "location_label": profile.location_label,
        "stack_label": profile.stack_label,
    }


@api_view(["GET"])
@ensure_csrf_cookie
def csrf_view(request):
    return Response({"csrfToken": get_token(request)})


@api_view(["GET"])
@permission_classes([AllowAny])
def public_profile(request):
    user = User.objects.filter(is_superuser=True, is_active=True).order_by("id").first()
    if not user:
        return Response(
            {
                "first_name": "",
                "last_name": "",
                "full_name": "",
                "email": "",
                "profile_picture": None,
                "job_title": "AI Automation Engineer",
                "hero_heading": "Engineering Agentic Intelligence",
                "hero_description": "",
                "resume_summary": "",
                "status_text": "AI Automation Engineer",
                "location_label": "PK // REMOTE",
                "stack_label": "Django • Next.js • Gemini",
            }
        )
    return Response(_build_profile_payload(user, request))


@api_view(["GET"])
@permission_classes([AllowAny])
def public_skills(request):
    skills = TechnicalSkill.objects.filter(is_active=True)
    return Response(
        [
            {
                "id": s.id,
                "skill_id": s.skill_id,
                "title": s.title,
                "subtitle": s.subtitle,
                "icon": s.icon,
                "tags": s.tags or [],
                "details": s.details,
                "mastery": s.mastery,
            }
            for s in skills
        ]
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def public_education(request):
    items = EducationItem.objects.filter(is_active=True)
    return Response(
        [
            {
                "id": e.id,
                "period": e.period,
                "institution": e.institution,
                "degree": e.degree,
                "specialization": e.specialization,
                "description": e.description,
                "tags": e.tags or [],
            }
            for e in items
        ]
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def public_hero_metrics(request):
    items = HeroMetric.objects.filter(is_active=True)
    return Response(
        [
            {
                "id": m.id,
                "value": m.value,
                "label": m.label,
                "color": m.color,
            }
            for m in items
        ]
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def public_social_links(request):
    items = SocialLink.objects.filter(is_active=True)
    return Response(
        [
            {
                "id": l.id,
                "platform": l.platform,
                "url": l.url,
                "label": l.label,
                "description": l.description,
            }
            for l in items
        ]
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def contact_submit(request):
    name = (request.data.get("name") or "").strip()
    email = (request.data.get("email") or "").strip()
    subject = (request.data.get("subject") or "").strip()
    message = (request.data.get("message") or "").strip()

    if not name or not email or not message:
        return Response(
            {"detail": "Name, email, and message are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
    return Response({"detail": "Message received."}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    email = (request.data.get("email") or "").strip().lower()
    password = request.data.get("password") or ""

    if not email or not password:
        return Response(
            {"detail": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(request, username=email, password=password)

    if user is None or not user.is_superuser or not user.is_active:
        return Response(
            {"detail": "Invalid credentials or insufficient permissions."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "detail": "Login successful.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": _build_profile_payload(user, request),
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    return Response({"detail": "Logged out."})


@api_view(["GET"])
@permission_classes([IsSuperUser])
def me_view(request):
    return Response(_build_profile_payload(request.user, request))


@api_view(["GET", "PATCH"])
@permission_classes([IsSuperUser])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def admin_profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "GET":
        return Response(_build_profile_payload(request.user, request))

    user = request.user
    for field in ["first_name", "last_name"]:
        val = request.data.get(field)
        if val is not None:
            setattr(user, field, str(val).strip())

    profile_fields = [
        "about_description",
        "job_title",
        "hero_heading",
        "hero_description",
        "resume_summary",
        "status_text",
        "location_label",
        "stack_label",
    ]
    updated = []
    for field in profile_fields:
        val = request.data.get(field)
        if val is not None:
            setattr(profile, field, str(val).strip())
            updated.append(field)

    if updated:
        updated.append("updated_at")
        profile.save(update_fields=updated)

    if not user.first_name:
        return Response(
            {"detail": "First name is required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.save(update_fields=["first_name", "last_name"])

    if request.FILES.get("profile_picture"):
        profile.profile_picture = request.FILES["profile_picture"]
        profile.save(update_fields=["profile_picture", "updated_at"])

    return Response(_build_profile_payload(user, request))


@api_view(["POST"])
@permission_classes([IsSuperUser])
def admin_password_view(request):
    form = ProfilePasswordForm(user=request.user, data=request.data)
    if not form.is_valid():
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    user = form.save()
    update_session_auth_hash(request, user)
    return Response({"detail": "Password updated successfully."})
