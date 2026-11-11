"""Attach bundled explainer videos/posters to services via default storage.

Idempotent: never replaces an existing cover, and never adds gallery rows
when a service already has media. Safe to re-run on deploy.
"""

from __future__ import annotations

from pathlib import Path

from django.core.files import File
from django.db import transaction

SEED_MEDIA_DIR = Path(__file__).resolve().parent / "seed_media"

SEED_SERVICE_MEDIA = [
    {
        "slug": "ai-automation",
        "cover": "ai-automation.jpg",
        "videos": [
            {
                "stem": "ai-automation",
                "file": "ai-automation.mp4",
                "poster": "ai-automation.jpg",
                "order": 0,
                "featured": True,
                "caption": (
                    "Explainer: a trigger starts an LLM agent that calls tools and APIs, "
                    "then logs the outcome to your CRM — with optional human approval, in n8n or Python."
                ),
                "alt_text": (
                    "Explainer video of an AI automation pipeline from trigger through "
                    "an LLM agent to CRM logging"
                ),
            },
            {
                "stem": "document-ai",
                "file": "document-ai.mp4",
                "poster": "document-ai.jpg",
                "order": 1,
                "featured": False,
                "caption": (
                    "Related: PDFs and scans in, structured fields out — extract, validate, "
                    "flag issues, then export to CSV, Excel, a database, or an API."
                ),
                "alt_text": (
                    "Explainer video of a document AI pipeline extracting and validating fields from PDFs"
                ),
            },
        ],
    },
    {
        "slug": "rag-ai-chatbots",
        "cover": "rag-chatbots.jpg",
        "videos": [
            {
                "stem": "rag-chatbots",
                "file": "rag-chatbots.mp4",
                "poster": "rag-chatbots.jpg",
                "order": 0,
                "featured": True,
                "caption": (
                    "Explainer: index your documents, retrieve matching passages, and answer "
                    "with citations — no source, no answer. Deploy on a website or Slack."
                ),
                "alt_text": (
                    "Explainer video of a retrieval-augmented chatbot citing source documents"
                ),
            },
        ],
    },
    {
        "slug": "ai-agents",
        "cover": "document-ai.jpg",
        "videos": [
            {
                "stem": "document-ai",
                "file": "document-ai.mp4",
                "poster": "document-ai.jpg",
                "order": 0,
                "featured": True,
                "caption": (
                    "Explainer: PDFs and scans in, structured fields out — extract, validate, "
                    "flag issues, then export to CSV, Excel, a database, or an API."
                ),
                "alt_text": (
                    "Explainer video of a document AI pipeline extracting and validating fields from PDFs"
                ),
            },
        ],
    },
    {
        "slug": "django-backend-development",
        "cover": "custom-development.jpg",
        "videos": [
            {
                "stem": "custom-development",
                "file": "custom-development.mp4",
                "poster": "custom-development.jpg",
                "order": 0,
                "featured": True,
                "caption": (
                    "Explainer: Django and DRF APIs, PostgreSQL, Next.js or Nuxt frontends, "
                    "tests, and a clean handover."
                ),
                "alt_text": (
                    "Explainer video of custom Django API and Next.js or Nuxt website development"
                ),
            },
        ],
    },
    {
        "slug": "api-integrations",
        "cover": "custom-development.jpg",
        "videos": [
            {
                "stem": "custom-development",
                "file": "custom-development.mp4",
                "poster": "custom-development.jpg",
                "order": 0,
                "featured": True,
                "caption": (
                    "Explainer: Django and DRF APIs, PostgreSQL, Next.js or Nuxt frontends, "
                    "tests, and a clean handover."
                ),
                "alt_text": (
                    "Explainer video of custom Django API and Next.js or Nuxt website development"
                ),
            },
        ],
    },
    {
        "slug": "nextjs-nuxt-websites",
        "cover": "custom-development.jpg",
        "videos": [
            {
                "stem": "custom-development",
                "file": "custom-development.mp4",
                "poster": "custom-development.jpg",
                "order": 0,
                "featured": True,
                "caption": (
                    "Explainer: Django and DRF APIs, PostgreSQL, Next.js or Nuxt frontends, "
                    "tests, and a clean handover."
                ),
                "alt_text": (
                    "Explainer video of custom Django API and Next.js or Nuxt website development"
                ),
            },
        ],
    },
    {
        "slug": "shopify-technical-seo-automation",
        "cover": "shopify-seo.jpg",
        "videos": [
            {
                "stem": "shopify-seo",
                "file": "shopify-seo.mp4",
                "poster": "shopify-seo.jpg",
                "order": 0,
                "featured": True,
                "caption": (
                    "Explainer: automated Shopify technical SEO — audit, prioritise, and apply "
                    "fixes such as redirects, schema, alt text, and metadata, then monitor on a "
                    "schedule. Rankings are not guaranteed."
                ),
                "alt_text": (
                    "Explainer video of automated Shopify technical SEO audit and fix workflow"
                ),
            },
        ],
    },
]


def _attach(field, source: Path, dest_name: str) -> None:
    with source.open("rb") as handle:
        field.save(dest_name, File(handle), save=False)


def seed_service_media(apps=None, media_dir: Path | None = None) -> dict:
    from django.apps import apps as django_apps

    apps = apps or django_apps
    media_dir = Path(media_dir) if media_dir else SEED_MEDIA_DIR
    Service = apps.get_model("core", "Service")
    ServiceMedia = apps.get_model("core", "ServiceMedia")

    covers_set = 0
    covers_skipped = 0
    media_created = 0
    media_skipped = 0
    missing_services = []

    for spec in SEED_SERVICE_MEDIA:
        service = Service.objects.filter(slug=spec["slug"]).first()
        if service is None:
            missing_services.append(spec["slug"])
            continue

        if service.cover_image:
            covers_skipped += 1
        else:
            cover_path = media_dir / spec["cover"]
            dest = f"{spec['slug']}{cover_path.suffix.lower()}"
            _attach(service.cover_image, cover_path, dest)
            service.save()
            covers_set += 1

        existing_media = ServiceMedia.objects.filter(service=service)
        if existing_media.exists():
            media_skipped += 1
            continue

        with transaction.atomic():
            for video in spec["videos"]:
                item = ServiceMedia(
                    service=service,
                    media_type="video",
                    order=video["order"],
                    featured=video["featured"],
                    caption=video["caption"],
                    alt_text=video["alt_text"],
                )
                video_path = media_dir / video["file"]
                poster_path = media_dir / video["poster"]
                _attach(
                    item.file,
                    video_path,
                    f"{spec['slug']}-{video['stem']}{video_path.suffix.lower()}",
                )
                _attach(
                    item.poster,
                    poster_path,
                    f"{spec['slug']}-{video['stem']}{poster_path.suffix.lower()}",
                )
                item.save()
                media_created += 1

    return {
        "covers_set": covers_set,
        "covers_skipped": covers_skipped,
        "media_created": media_created,
        "media_skipped": media_skipped,
        "missing_services": missing_services,
    }
