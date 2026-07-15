import os

from core.models import Project, ProjectImage


def _absolute_media_url(request, image_field) -> str | None:
    if not image_field:
        return None

    raw_url = image_field.url
    # Cloudinary (and similar) already return absolute URLs
    if raw_url.startswith("http://") or raw_url.startswith("https://"):
        return raw_url

    public_base = (
        os.getenv("PUBLIC_API_URL", "").strip()
        or os.getenv("BACKEND_PUBLIC_URL", "").strip()
    )
    if public_base:
        return f"{public_base.rstrip('/')}{raw_url}"

    absolute = request.build_absolute_uri(raw_url)

    # PythonAnywhere / reverse proxies often report http; force https for browsers
    host = request.get_host().lower()
    force_https = (
        request.is_secure()
        or os.getenv("FORCE_HTTPS_MEDIA", "").lower() in ("true", "1", "yes")
        or "pythonanywhere.com" in host
        or bool(os.getenv("VERCEL"))
    )
    if force_https and absolute.startswith("http://"):
        absolute = "https://" + absolute[len("http://") :]

    return absolute


def serialize_project_image(image: ProjectImage, request) -> dict:
    return {
        "id": image.id,
        "url": _absolute_media_url(request, image.image),
        "order": image.order,
        "alt_text": image.alt_text,
    }


def serialize_project(project: Project, request) -> dict:
    images = [
        item
        for item in (serialize_project_image(image, request) for image in project.images.all())
        if item["url"]
    ]
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
