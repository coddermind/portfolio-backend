import os

from core.models import Project, ProjectImage


def _absolute_media_url(request, image_field) -> str | None:
    if not image_field:
        return None

    raw_url = image_field.url
    if raw_url.startswith("http://") or raw_url.startswith("https://"):
        return raw_url

    public_base = os.getenv("PUBLIC_API_URL", "").strip()
    if public_base:
        return f"{public_base.rstrip('/')}{raw_url}"

    absolute = request.build_absolute_uri(raw_url)

    force_https = request.is_secure() or os.getenv(
        "FORCE_HTTPS_MEDIA", ""
    ).lower() in ("true", "1", "yes")
    if force_https and absolute.startswith("http://"):
        absolute = "https://" + absolute[len("http://"):]

    return absolute


def serialize_project_image(image: ProjectImage, request) -> dict:
    return {
        "id": image.id,
        "url": _absolute_media_url(request, image.image),
        "order": image.order,
        "alt_text": image.alt_text,
    }


def serialize_project(project: Project, request) -> dict:
    image_url = _absolute_media_url(request, project.image) if project.image else None

    return {
        "id": project.id,
        "order": project.order,
        "slug": project.slug,
        "title": project.title,
        "year": project.year,
        "category": project.category,
        "short_description": project.short_description,
        "full_description": project.full_description,
        "image": image_url,
        "tags": project.tags or [],
        "goal": project.goal,
        "result": project.result,
        "architecture": project.architecture or [],
        "pipeline_steps": project.pipeline_steps or [],
        "metrics": project.metrics or [],
        "is_active": project.is_active,
    }
