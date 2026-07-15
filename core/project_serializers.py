from core.models import Project, ProjectImage


def _absolute_media_url(request, image_field) -> str | None:
    if not image_field:
        return None
    return request.build_absolute_uri(image_field.url)


def serialize_project_image(image: ProjectImage, request) -> dict:
    return {
        "id": image.id,
        "url": _absolute_media_url(request, image.image),
        "order": image.order,
        "alt_text": image.alt_text,
    }


def serialize_project(project: Project, request) -> dict:
    images = [serialize_project_image(image, request) for image in project.images.all()]
    cover = images[0]["url"] if images else None

    return {
        "id": project.id,
        "order": project.order,
        "slug": project.slug,
        "title": project.title,
        "year": project.year,
        "short_description": project.short_description,
        "architectural_vision": project.architectural_vision,
        "tags": project.tags,
        "icon": project.icon,
        "color": project.color,
        "featured": project.featured,
        "timeline": project.timeline,
        "lead_role": project.lead_role,
        "environment": project.environment,
        "goal": project.goal,
        "result": project.result,
        "is_active": project.is_active,
        "images": images,
        "image": cover,
    }
