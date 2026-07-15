import json

from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import Project, ProjectImage
from core.permissions import IsSuperUser
from core.project_serializers import serialize_project


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


def _apply_project_fields(project: Project, data) -> None:
    field_map = {
        "order": ("order", _parse_int),
        "slug": ("slug", str),
        "title": ("title", str),
        "year": ("year", _parse_int),
        "short_description": ("short_description", str),
        "architectural_vision": ("architectural_vision", str),
        "icon": ("icon", str),
        "color": ("color", str),
        "timeline": ("timeline", str),
        "lead_role": ("lead_role", str),
        "environment": ("environment", str),
        "goal": ("goal", str),
        "result": ("result", str),
    }

    for key, (attr, caster) in field_map.items():
        if key in data:
            setattr(project, attr, caster(data.get(key)))

    if "tags" in data:
        project.tags = _parse_tags(data.get("tags"))

    if "featured" in data:
        project.featured = _parse_bool(data.get("featured"))

    if "is_active" in data:
        project.is_active = _parse_bool(data.get("is_active"), default=True)


def _attach_images(project: Project, request) -> None:
    files = request.FILES.getlist("images")
    if not files:
        return

    next_order = project.images.count()
    for index, uploaded in enumerate(files):
        ProjectImage.objects.create(
            project=project,
            image=uploaded,
            order=next_order + index,
        )


def _delete_images(project: Project, data) -> None:
    delete_ids = data.get("delete_image_ids")
    if not delete_ids:
        return

    if isinstance(delete_ids, str):
        try:
            delete_ids = json.loads(delete_ids)
        except json.JSONDecodeError:
            delete_ids = []

    if isinstance(delete_ids, list) and delete_ids:
        ProjectImage.objects.filter(project=project, id__in=delete_ids).delete()


@api_view(["GET"])
@permission_classes([AllowAny])
def public_projects_list(request):
    projects = Project.objects.filter(is_active=True)
    return Response([serialize_project(project, request) for project in projects])


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
        return Response([serialize_project(project, request) for project in projects])

    slug = (request.data.get("slug") or "").strip()
    title = (request.data.get("title") or "").strip()
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

    project = Project(
        slug=slug,
        title=title,
        year=_parse_int(request.data.get("year"), default=2025),
        short_description=request.data.get("short_description", ""),
        architectural_vision=request.data.get("architectural_vision", ""),
        tags=_parse_tags(request.data.get("tags")),
        icon=request.data.get("icon", "Activity"),
        color=request.data.get("color", "#a855f7"),
        featured=_parse_bool(request.data.get("featured")),
        timeline=request.data.get("timeline", ""),
        lead_role=request.data.get("lead_role", ""),
        environment=request.data.get("environment", ""),
        goal=request.data.get("goal", ""),
        result=request.data.get("result", ""),
        order=_parse_int(request.data.get("order"), default=Project.objects.count() + 1),
        is_active=_parse_bool(request.data.get("is_active"), default=True),
    )
    project.save()
    _attach_images(project, request)

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

    new_slug = request.data.get("slug")
    if new_slug and new_slug != project.slug:
        if Project.objects.filter(slug=new_slug).exclude(pk=project.pk).exists():
            return Response(
                {"detail": "A project with this slug already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    _apply_project_fields(project, request.data)
    project.save()
    _delete_images(project, request.data)
    _attach_images(project, request)

    return Response(serialize_project(project, request))
