import json
import logging
from pathlib import Path

from django.conf import settings
from django.utils.text import slugify
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import Project
from core.permissions import IsSuperUser
from core.project_serializers import serialize_project

logger = logging.getLogger(__name__)


def _parse_tags(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        if not value.strip():
            return []
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, list) else []
        except json.JSONDecodeError:
            return [item.strip() for item in value.split(",") if item.strip()]
    return []


def _parse_json_field(value, default=None):
    if default is None:
        default = []
    if value is None:
        return default
    if isinstance(value, (list, dict)):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return default
    return default


def _parse_bool(value, default=False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    return str(value).lower() in {"1", "true", "yes", "on"}


def _parse_int(value, default=0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _normalize_slug(raw_slug: str, fallback_title: str = "") -> str:
    cleaned = slugify((raw_slug or "").strip())
    if cleaned:
        return cleaned
    return slugify((fallback_title or "").strip())


def _ensure_media_dirs() -> None:
    if settings.USE_REMOTE_MEDIA:
        return
    media_root = Path(settings.MEDIA_ROOT)
    (media_root / "projects").mkdir(parents=True, exist_ok=True)
    (media_root / "profiles").mkdir(parents=True, exist_ok=True)
    (media_root / "cvs").mkdir(parents=True, exist_ok=True)


def _apply_project_fields(project: Project, data) -> None:
    str_fields = [
        "title", "short_description", "full_description",
        "category", "goal", "result",
    ]
    for key in str_fields:
        if key in data:
            setattr(project, key, str(data.get(key, "")))

    if "order" in data:
        project.order = _parse_int(data.get("order"))

    if "year" in data:
        project.year = _parse_int(data.get("year"))

    if "slug" in data:
        project.slug = _normalize_slug(data.get("slug") or "", project.title)

    if "tags" in data:
        project.tags = _parse_tags(data.get("tags"))

    for json_field in ["architecture", "pipeline_steps", "metrics"]:
        if json_field in data:
            setattr(project, json_field, _parse_json_field(data.get(json_field)))

    if "is_active" in data:
        project.is_active = _parse_bool(data.get("is_active"), default=True)


@api_view(["GET"])
@permission_classes([AllowAny])
def public_projects_list(request):
    projects = Project.objects.filter(is_active=True)
    return Response([serialize_project(p, request) for p in projects])


@api_view(["GET"])
@permission_classes([AllowAny])
def public_project_detail(request, slug):
    try:
        project = Project.objects.get(slug=slug, is_active=True)
    except Project.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(serialize_project(project, request))


@api_view(["GET", "POST"])
@permission_classes([IsSuperUser])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def admin_projects_list_view(request):
    if request.method == "GET":
        projects = Project.objects.all()
        return Response([serialize_project(p, request) for p in projects])

    title = (request.data.get("title") or "").strip()
    slug = _normalize_slug(request.data.get("slug") or "", title)

    if not slug or not title:
        return Response(
            {"detail": "Slug and title are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if Project.objects.filter(slug=slug).exists():
        return Response(
            {"detail": "A project with this slug already exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    _ensure_media_dirs()

    project = Project(
        slug=slug,
        title=title,
        year=_parse_int(request.data.get("year"), default=2025),
        category=request.data.get("category", "AI Agents"),
        short_description=request.data.get("short_description", ""),
        full_description=request.data.get("full_description", ""),
        tags=_parse_tags(request.data.get("tags")),
        goal=request.data.get("goal", ""),
        result=request.data.get("result", ""),
        architecture=_parse_json_field(request.data.get("architecture")),
        pipeline_steps=_parse_json_field(request.data.get("pipeline_steps")),
        metrics=_parse_json_field(request.data.get("metrics")),
        order=_parse_int(request.data.get("order"), default=Project.objects.count() + 1),
        is_active=_parse_bool(request.data.get("is_active"), default=True),
    )

    if request.FILES.get("image"):
        project.image = request.FILES["image"]

    try:
        project.save()
    except Exception as exc:
        logger.exception("Failed to create project")
        return Response(
            {"detail": f"Could not save project: {exc}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(serialize_project(project, request), status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsSuperUser])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def admin_projects_detail_view(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(serialize_project(project, request))

    if request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    original_slug = project.slug
    _apply_project_fields(project, request.data)

    if project.slug != original_slug and Project.objects.filter(slug=project.slug).exclude(pk=project.pk).exists():
        return Response(
            {"detail": "A project with this slug already exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if request.FILES.get("image"):
        _ensure_media_dirs()
        project.image = request.FILES["image"]

    try:
        project.save()
    except Exception as exc:
        logger.exception("Failed to update project %s", project.pk)
        return Response(
            {"detail": f"Could not update project: {exc}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(serialize_project(project, request))
