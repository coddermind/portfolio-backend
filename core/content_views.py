from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.content_serializers import (
    get_public_home_content,
    serialize_persona,
    serialize_philosophy,
    serialize_skill,
)
from core.models import PersonaSection, PhilosophyParagraph, TechnicalSkill
from core.permissions import IsSuperUser


@api_view(["GET"])
@permission_classes([AllowAny])
def public_home_content(request):
    return Response(get_public_home_content())


@api_view(["GET", "PATCH"])
@permission_classes([IsSuperUser])
def admin_persona_view(request):
    persona, _ = PersonaSection.objects.get_or_create(
        pk=1,
        defaults={
            "heading": "Engineering Agentic Intelligence",
            "description": "",
            "image_role_label": "AI Automation Engineer",
        },
    )

    if request.method == "GET":
        return Response(serialize_persona(persona))

    for field in ("heading", "description", "image_role_label"):
        if field in request.data:
            setattr(persona, field, request.data[field])
    persona.save()
    return Response(serialize_persona(persona))


@api_view(["GET", "POST"])
@permission_classes([IsSuperUser])
def admin_philosophy_list_view(request):
    if request.method == "GET":
        items = PhilosophyParagraph.objects.all()
        return Response([serialize_philosophy(item) for item in items])

    order = request.data.get("order") or (PhilosophyParagraph.objects.count() + 1)
    paragraph = PhilosophyParagraph.objects.create(
        order=order,
        content=request.data.get("content", ""),
        is_active=request.data.get("is_active", True),
    )
    return Response(serialize_philosophy(paragraph), status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsSuperUser])
def admin_philosophy_detail_view(request, pk):
    try:
        paragraph = PhilosophyParagraph.objects.get(pk=pk)
    except PhilosophyParagraph.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(serialize_philosophy(paragraph))

    if request.method == "DELETE":
        paragraph.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    for field in ("order", "content", "is_active"):
        if field in request.data:
            setattr(paragraph, field, request.data[field])
    paragraph.save()
    return Response(serialize_philosophy(paragraph))


@api_view(["GET", "POST"])
@permission_classes([IsSuperUser])
def admin_skills_list_view(request):
    if request.method == "GET":
        items = TechnicalSkill.objects.all()
        return Response([serialize_skill(item) for item in items])

    skill = TechnicalSkill.objects.create(
        order=request.data.get("order", TechnicalSkill.objects.count() + 1),
        skill_id=request.data.get("skill_id", ""),
        title=request.data.get("title", ""),
        subtitle=request.data.get("subtitle", ""),
        proficiency=request.data.get("proficiency", 0),
        color=request.data.get("color", "#a855f7"),
        icon=request.data.get("icon", "Bot"),
        tags=request.data.get("tags", []),
        is_active=request.data.get("is_active", True),
    )
    return Response(serialize_skill(skill), status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsSuperUser])
def admin_skills_detail_view(request, pk):
    try:
        skill = TechnicalSkill.objects.get(pk=pk)
    except TechnicalSkill.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(serialize_skill(skill))

    if request.method == "DELETE":
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    for field in (
        "order",
        "skill_id",
        "title",
        "subtitle",
        "proficiency",
        "color",
        "icon",
        "tags",
        "is_active",
    ):
        if field in request.data:
            setattr(skill, field, request.data[field])
    skill.save()
    return Response(serialize_skill(skill))
