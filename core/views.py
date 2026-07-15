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
from core.models import Profile
from core.permissions import IsSuperUser

User = get_user_model()

DEFAULT_ABOUT_DESCRIPTION = (
    "An Artificial Intelligence student and Software Engineer who believes that "
    "code is a medium for art, and data is the soul of modern intelligence."
)


def _build_profile_payload(user, request):
    profile, _ = Profile.objects.get_or_create(user=user)
    picture_url = None
    if profile.profile_picture:
        picture_url = request.build_absolute_uri(profile.profile_picture.url)

    about_description = profile.about_description.strip() or DEFAULT_ABOUT_DESCRIPTION

    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "full_name": user.full_name,
        "email": user.email,
        "profile_picture": picture_url,
        "about_description": about_description,
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
                "email": None,
                "profile_picture": None,
                "about_description": DEFAULT_ABOUT_DESCRIPTION,
            }
        )
    return Response(_build_profile_payload(user, request))


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
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    about_description = request.data.get("about_description")

    if first_name is not None:
        user.first_name = str(first_name).strip()
    if last_name is not None:
        user.last_name = str(last_name).strip()
    if about_description is not None:
        profile.about_description = str(about_description).strip()
        profile.save(update_fields=["about_description", "updated_at"])

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
