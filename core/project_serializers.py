from core.models import Project, ProjectImage
from core.utils import absolute_media_url as _absolute_media_url


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
