from pathlib import Path

from django.core.exceptions import ValidationError

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov"}
MEDIA_EXTENSIONS = IMAGE_EXTENSIONS | VIDEO_EXTENSIONS

MAX_IMAGE_BYTES = 10 * 1024 * 1024  # 10 MB
MAX_VIDEO_BYTES = 50 * 1024 * 1024  # 50 MB


def _extension(name: str) -> str:
    return Path(name or "").suffix.lower()


def validate_image_file(file) -> None:
    if not file:
        return
    ext = _extension(getattr(file, "name", ""))
    if ext not in IMAGE_EXTENSIONS:
        raise ValidationError(
            f"Unsupported image type {ext or '(none)'}. "
            f"Allowed: {', '.join(sorted(IMAGE_EXTENSIONS))}."
        )
    size = getattr(file, "size", 0) or 0
    if size > MAX_IMAGE_BYTES:
        raise ValidationError("Image must be 10 MB or smaller.")


def validate_media_file(file) -> None:
    if not file:
        return
    ext = _extension(getattr(file, "name", ""))
    if ext not in MEDIA_EXTENSIONS:
        raise ValidationError(
            f"Unsupported file type {ext or '(none)'}. "
            f"Images: {', '.join(sorted(IMAGE_EXTENSIONS))}. "
            f"Videos: {', '.join(sorted(VIDEO_EXTENSIONS))}."
        )
    size = getattr(file, "size", 0) or 0
    if ext in VIDEO_EXTENSIONS and size > MAX_VIDEO_BYTES:
        raise ValidationError("Video must be 50 MB or smaller.")
    if ext in IMAGE_EXTENSIONS and size > MAX_IMAGE_BYTES:
        raise ValidationError("Image must be 10 MB or smaller.")


def media_type_from_filename(name: str) -> str:
    ext = _extension(name)
    if ext in VIDEO_EXTENSIONS:
        return "video"
    return "image"
