from core.models import Service, ServiceMedia
from core.utils import absolute_media_url


def serialize_service_media(item: ServiceMedia, request) -> dict:
    return {
        "id": item.id,
        "order": item.order,
        "media_type": item.media_type,
        "url": absolute_media_url(request, item.file),
        "poster_url": absolute_media_url(request, item.poster) if item.poster else None,
        "caption": item.caption,
        "alt_text": item.alt_text,
        "featured": item.featured,
    }


def serialize_service(service: Service, request) -> dict:
    return {
        "id": service.id,
        "order": service.order,
        "slug": service.slug,
        "title": service.title,
        "tagline": service.tagline,
        "description": service.description,
        "icon": service.icon,
        "cta_text": service.cta_text,
        "tech_stack": service.tech_stack or [],
        "cover_image": (
            absolute_media_url(request, service.cover_image)
            if service.cover_image
            else None
        ),
        "is_published": service.is_published,
        "deliverables": [
            {
                "id": item.id,
                "order": item.order,
                "title": item.title,
                "description": item.description,
            }
            for item in service.deliverables.all()
        ],
        "process_steps": [
            {
                "id": item.id,
                "order": item.order,
                "title": item.title,
                "description": item.description,
            }
            for item in service.process_steps.all()
        ],
        "use_cases": [
            {
                "id": item.id,
                "order": item.order,
                "title": item.title,
                "description": item.description,
            }
            for item in service.use_cases.all()
        ],
        "faqs": [
            {
                "id": item.id,
                "order": item.order,
                "question": item.question,
                "answer": item.answer,
            }
            for item in service.faqs.all()
        ],
        "media": [serialize_service_media(item, request) for item in service.media.all()],
    }
