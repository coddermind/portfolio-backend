import mimetypes
from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET


@require_GET
@cache_control(public=True, max_age=86400)
def serve_local_media(request, path):
    if settings.USE_CLOUDINARY:
        raise Http404()

    media_root = Path(settings.MEDIA_ROOT).resolve()
    file_path = (media_root / path).resolve()

    if not file_path.is_file():
        raise Http404()

    try:
        file_path.relative_to(media_root)
    except ValueError as exc:
        raise Http404() from exc

    content_type, _ = mimetypes.guess_type(str(file_path))
    return FileResponse(
        file_path.open("rb"),
        content_type=content_type or "application/octet-stream",
    )
