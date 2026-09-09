from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.models import EducationItem
from core.permissions import IsSuperUser


def _parse_tags(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        if not value.strip():
            return []
        import json

        try:
            parsed = json.loads(value)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        except json.JSONDecodeError:
            pass
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


def serialize_education(item: EducationItem) -> dict:
    return {
        "id": item.id,
        "order": item.order,
        "period": item.period,
        "institution": item.institution,
        "degree": item.degree,
        "specialization": item.specialization,
        "description": item.description,
        "tags": item.tags or [],
        "is_active": item.is_active,
    }


def _apply_education_fields(item: EducationItem, data) -> None:
    for key in ["period", "institution", "degree", "specialization", "description"]:
        if key in data:
            setattr(item, key, str(data.get(key, "")).strip())

    if "order" in data:
        item.order = _parse_int(data.get("order"))

    if "tags" in data:
        item.tags = _parse_tags(data.get("tags"))

    if "is_active" in data:
        item.is_active = _parse_bool(data.get("is_active"), default=True)


@api_view(["GET", "POST"])
@permission_classes([IsSuperUser])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def admin_education_list_view(request):
    if request.method == "GET":
        items = EducationItem.objects.all()
        return Response([serialize_education(item) for item in items])

    institution = (request.data.get("institution") or "").strip()
    degree = (request.data.get("degree") or "").strip()
    period = (request.data.get("period") or "").strip()

    if not institution or not degree or not period:
        return Response(
            {"detail": "Period, institution, and degree are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    item = EducationItem.objects.create(
        order=_parse_int(request.data.get("order"), default=EducationItem.objects.count() + 1),
        period=period,
        institution=institution,
        degree=degree,
        specialization=(request.data.get("specialization") or "").strip(),
        description=(request.data.get("description") or "").strip(),
        tags=_parse_tags(request.data.get("tags")),
        is_active=_parse_bool(request.data.get("is_active"), default=True),
    )
    return Response(serialize_education(item), status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsSuperUser])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def admin_education_detail_view(request, pk):
    try:
        item = EducationItem.objects.get(pk=pk)
    except EducationItem.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(serialize_education(item))

    if request.method == "DELETE":
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    _apply_education_fields(item, request.data)

    if not item.institution or not item.degree or not item.period:
        return Response(
            {"detail": "Period, institution, and degree are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    item.save()
    return Response(serialize_education(item))
