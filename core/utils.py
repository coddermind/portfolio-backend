import os


def split_full_name(full_name: str) -> tuple[str, str]:
    parts = full_name.strip().split(None, 1)
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], parts[1]


def absolute_media_url(request, file_field) -> str | None:
    if not file_field:
        return None

    raw_url = file_field.url
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
