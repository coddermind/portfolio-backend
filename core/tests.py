import io
import json
from unittest.mock import patch

from django.apps import apps
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, override_settings
from PIL import Image
from rest_framework.test import APIClient

from core.content_defaults import DEFAULT_PROJECTS
from core.management.commands.anonymize_client_projects import (
    CLIENT_NAME_PATTERNS,
    PROJECT_RENAMES,
    anonymize_client_projects,
)
from core.models import Project, ProjectImage, Service, ServiceMedia
from core.service_defaults import DEFAULT_SERVICES, seed_services
from core.service_media_seed import SEED_MEDIA_DIR, SEED_SERVICE_MEDIA, seed_service_media


def _blob_has_client_name(value) -> bool:
    text = value if isinstance(value, str) else json.dumps(value)
    return any(pattern.search(text) for pattern in CLIENT_NAME_PATTERNS)


class AnonymizeClientProjectsTests(TestCase):
    def _make_project(self, spec, extra_description=""):
        needles = spec["title_needles"]
        title = needles[0].title()
        project = Project.objects.create(
            slug=spec["old_slugs"][0],
            title=title,
            year=2026,
            category="AI Agents",
            short_description=extra_description or title,
            full_description=extra_description or title,
            goal=title,
            result=title,
            tags=[title, "Django"],
        )
        ProjectImage.objects.create(project=project, alt_text=title, order=0)
        return project

    def test_seed_defaults_have_no_client_names(self):
        blob = json.dumps(DEFAULT_PROJECTS)
        self.assertFalse(_blob_has_client_name(blob))

    def test_renames_three_projects_and_is_idempotent(self):
        seo_product_needle = PROJECT_RENAMES[2]["title_needles"][0]
        for spec in PROJECT_RENAMES:
            extra = f"audits via {seo_product_needle} integration"
            self._make_project(spec, extra_description=extra)

        logs = anonymize_client_projects(apps, dry_run=False)
        self.assertTrue(any("Updated" in line for line in logs))

        for spec in PROJECT_RENAMES:
            project = Project.objects.get(slug=spec["new_slug"])
            self.assertEqual(project.title, spec["new_title"])
            self.assertEqual(Project.objects.filter(slug=spec["old_slugs"][0]).count(), 0)
            self.assertFalse(_blob_has_client_name(project.title))
            self.assertFalse(_blob_has_client_name(project.short_description))
            self.assertFalse(_blob_has_client_name(project.full_description))
            self.assertFalse(_blob_has_client_name(project.goal))
            self.assertFalse(_blob_has_client_name(project.result))
            self.assertFalse(_blob_has_client_name(project.tags))
            alt = project.images.first().alt_text
            self.assertFalse(_blob_has_client_name(alt))

        logs_again = anonymize_client_projects(apps, dry_run=False)
        self.assertTrue(all("Already anonymized" in line or "No database row" in line for line in logs_again))
        self.assertEqual(Project.objects.count(), 3)

    def test_dry_run_does_not_write(self):
        spec = PROJECT_RENAMES[0]
        project = self._make_project(spec)
        anonymize_client_projects(apps, dry_run=True)
        project.refresh_from_db()
        self.assertEqual(project.slug, spec["old_slugs"][0])

    def test_management_command(self):
        spec = PROJECT_RENAMES[1]
        self._make_project(spec)
        call_command("anonymize_client_projects")
        self.assertTrue(Project.objects.filter(slug=spec["new_slug"]).exists())


def _png_file(name="cover.png"):
    buffer = io.BytesIO()
    Image.new("RGB", (8, 8), color=(76, 215, 246)).save(buffer, format="PNG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/png")


class ServiceModelAndAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.published = Service.objects.create(
            slug="test-published-service",
            title="AI Automation & Workflow Automation",
            tagline="Replace copy-paste work.",
            description="Build reliable pipelines.",
            tech_stack=["Django", "Python"],
            cta_text="Start a conversation",
            icon="account_tree",
            order=0,
            is_published=True,
            cover_image=_png_file(),
        )
        self.published.deliverables.create(
            order=0, title="Mapped workflow", description="Current steps."
        )
        self.published.process_steps.create(
            order=0, title="Walk the process", description="Start from today."
        )
        self.published.use_cases.create(
            order=0, title="Intake", description="Forms instead of email."
        )
        self.published.faqs.create(
            order=0, question="Do you use n8n?", answer="When it fits."
        )
        self.published.media.create(
            order=0,
            media_type="image",
            file=_png_file("gallery.png"),
            caption="Dashboard",
            alt_text="Automation dashboard screenshot",
            featured=True,
        )
        self.draft = Service.objects.create(
            slug="secret-internal",
            title="Unpublished",
            tagline="Hidden",
            description="Not public.",
            order=9,
            is_published=False,
        )

    def test_list_returns_only_published_with_nested_payload(self):
        response = self.client.get("/api/services/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        slugs = [item["slug"] for item in data]
        self.assertIn(self.published.slug, slugs)
        self.assertNotIn(self.draft.slug, slugs)
        item = next(row for row in data if row["slug"] == self.published.slug)
        self.assertEqual(item["title"], self.published.title)
        self.assertEqual(item["tagline"], self.published.tagline)
        self.assertEqual(item["cta_text"], "Start a conversation")
        self.assertEqual(item["tech_stack"], ["Django", "Python"])
        self.assertTrue(item["cover_image"].startswith("http"))
        self.assertEqual(item["deliverables"][0]["title"], "Mapped workflow")
        self.assertEqual(item["process_steps"][0]["title"], "Walk the process")
        self.assertEqual(item["use_cases"][0]["title"], "Intake")
        self.assertEqual(item["faqs"][0]["question"], "Do you use n8n?")
        self.assertEqual(item["media"][0]["media_type"], "image")
        self.assertTrue(item["media"][0]["featured"])
        self.assertTrue(item["media"][0]["url"].startswith("http"))

    def test_detail_by_slug_and_unpublished_404(self):
        ok = self.client.get("/api/services/test-published-service/")
        self.assertEqual(ok.status_code, 200)
        self.assertEqual(ok.json()["slug"], "test-published-service")

        hidden = self.client.get("/api/services/secret-internal/")
        self.assertEqual(hidden.status_code, 404)

        missing = self.client.get("/api/services/does-not-exist/")
        self.assertEqual(missing.status_code, 404)

    def test_existing_project_endpoints_still_work(self):
        Project.objects.create(
            slug="voice-enabled-event-booking",
            title="Voice-Enabled Event Booking",
            year=2026,
            short_description="Voice booking.",
        )
        listing = self.client.get("/api/projects/")
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(listing.json()[0]["slug"], "voice-enabled-event-booking")

        detail = self.client.get("/api/projects/voice-enabled-event-booking/")
        self.assertEqual(detail.status_code, 200)

    @override_settings(MEDIA_URL="/api/media/")
    def test_absolute_media_urls_use_public_api_url(self):
        with patch.dict("os.environ", {"PUBLIC_API_URL": "https://api.example.com"}):
            response = self.client.get("/api/services/test-published-service/")
        cover = response.json()["cover_image"]
        self.assertTrue(cover.startswith("https://api.example.com/"))

    def test_media_validation_rejects_bad_type_and_oversize(self):
        item = ServiceMedia(
            service=self.published,
            file=SimpleUploadedFile("notes.txt", b"hello", content_type="text/plain"),
        )
        with self.assertRaises(ValidationError):
            item.full_clean()

        with patch("core.validators.MAX_IMAGE_BYTES", 10):
            huge = ServiceMedia(
                service=self.published,
                file=SimpleUploadedFile("huge.png", b"x" * 20, content_type="image/png"),
            )
            with self.assertRaises(ValidationError):
                huge.full_clean()

    def test_video_type_is_inferred(self):
        item = ServiceMedia(
            service=self.published,
            media_type="image",
            file=SimpleUploadedFile("walkthrough.mp4", b"00", content_type="video/mp4"),
        )
        item.full_clean()
        self.assertEqual(item.media_type, "video")

    def test_seed_is_idempotent_and_has_no_client_names(self):
        blob = json.dumps(DEFAULT_SERVICES)
        self.assertFalse(_blob_has_client_name(blob))
        self.assertGreaterEqual(len(DEFAULT_SERVICES), 7)
        self.assertTrue(
            any(spec["slug"] == "shopify-technical-seo-automation" for spec in DEFAULT_SERVICES)
        )

        first = seed_services()
        self.assertEqual(first["total"], len(DEFAULT_SERVICES))
        self.assertEqual(first["created"] + first["updated"], len(DEFAULT_SERVICES))
        count_after_first = Service.objects.count()
        faq_count = sum(service.faqs.count() for service in Service.objects.all())

        second = seed_services()
        self.assertEqual(second["created"], 0)
        self.assertEqual(Service.objects.count(), count_after_first)
        self.assertEqual(
            sum(service.faqs.count() for service in Service.objects.all()),
            faq_count,
        )
        slugs = set(Service.objects.values_list("slug", flat=True))
        for spec in DEFAULT_SERVICES:
            self.assertIn(spec["slug"], slugs)
            service = Service.objects.get(slug=spec["slug"])
            self.assertEqual(service.title, spec["title"])
            self.assertTrue(service.deliverables.exists())
            self.assertTrue(service.process_steps.exists())
            self.assertTrue(service.use_cases.exists())
            self.assertTrue(service.faqs.exists())


def _expected_media_count():
    return sum(len(spec["videos"]) for spec in SEED_SERVICE_MEDIA)


class ServiceMediaSeedTests(TestCase):
    def test_seed_files_exist(self):
        self.assertTrue(SEED_MEDIA_DIR.is_dir())
        for spec in SEED_SERVICE_MEDIA:
            self.assertTrue((SEED_MEDIA_DIR / spec["cover"]).is_file(), spec["cover"])
            for video in spec["videos"]:
                self.assertTrue((SEED_MEDIA_DIR / video["file"]).is_file(), video["file"])
                self.assertTrue((SEED_MEDIA_DIR / video["poster"]).is_file(), video["poster"])

    def test_migration_attached_cover_and_videos(self):
        for spec in SEED_SERVICE_MEDIA:
            service = Service.objects.get(slug=spec["slug"])
            self.assertTrue(service.cover_image)
            videos = list(service.media.filter(media_type="video"))
            self.assertEqual(len(videos), len(spec["videos"]))
            featured = [item for item in videos if item.featured]
            self.assertEqual(len(featured), 1)
            for item in videos:
                self.assertTrue(item.file)
                self.assertTrue(item.poster)
                self.assertTrue(item.caption)
                self.assertTrue(item.alt_text)

    def test_seed_media_is_idempotent_and_preserves_admin_edits(self):
        before_covers = list(
            Service.objects.filter(
                slug__in=[spec["slug"] for spec in SEED_SERVICE_MEDIA]
            ).values_list("slug", "cover_image")
        )
        before_media = ServiceMedia.objects.count()

        again = seed_service_media()
        self.assertEqual(again["covers_set"], 0)
        self.assertEqual(again["media_created"], 0)
        self.assertEqual(ServiceMedia.objects.count(), before_media)
        self.assertEqual(
            list(
                Service.objects.filter(
                    slug__in=[spec["slug"] for spec in SEED_SERVICE_MEDIA]
                ).values_list("slug", "cover_image")
            ),
            before_covers,
        )

        service = Service.objects.get(slug="rag-ai-chatbots")
        service.cover_image.save("admin-keep.png", _png_file("admin-keep.png"), save=True)
        kept_name = service.cover_image.name
        ServiceMedia.objects.create(
            service=service,
            media_type="image",
            file=_png_file("admin-gallery.png"),
            caption="Owner upload",
            alt_text="Owner-uploaded still",
            order=9,
        )
        media_after_edit = ServiceMedia.objects.filter(service=service).count()

        seed_service_media()
        service.refresh_from_db()
        self.assertEqual(service.cover_image.name, kept_name)
        self.assertEqual(
            ServiceMedia.objects.filter(service=service).count(),
            media_after_edit,
        )

    def test_empty_service_receives_media_then_stops(self):
        service = Service.objects.get(slug="ai-agents")
        service.cover_image.delete(save=True)
        ServiceMedia.objects.filter(service=service).delete()
        service.refresh_from_db()
        self.assertFalse(service.cover_image)
        self.assertFalse(service.media.exists())

        first = seed_service_media()
        self.assertGreaterEqual(first["covers_set"], 1)
        self.assertGreaterEqual(first["media_created"], 1)
        service.refresh_from_db()
        self.assertTrue(service.cover_image)
        self.assertTrue(service.media.exists())
        media_count = service.media.count()

        second = seed_service_media()
        self.assertEqual(second["media_created"], 0)
        service.refresh_from_db()
        self.assertEqual(service.media.count(), media_count)

    def test_api_returns_absolute_cover_and_media_urls(self):
        client = APIClient()
        with patch.dict("os.environ", {"PUBLIC_API_URL": "https://api.muhammadabrar.com"}):
            response = client.get("/api/services/shopify-technical-seo-automation/")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["cover_image"].startswith("https://"))
        self.assertGreaterEqual(len(payload["media"]), 1)
        video = payload["media"][0]
        self.assertEqual(video["media_type"], "video")
        self.assertTrue(video["featured"])
        self.assertTrue(video["url"].startswith("https://"))
        self.assertTrue(video["poster_url"].startswith("https://"))
        self.assertIn("shopify", video["alt_text"].lower())

    def test_seed_copy_has_no_client_names(self):
        shopify = next(
            spec
            for spec in DEFAULT_SERVICES
            if spec["slug"] == "shopify-technical-seo-automation"
        )
        self.assertFalse(_blob_has_client_name(json.dumps(shopify)))
        self.assertFalse(_blob_has_client_name(json.dumps(SEED_SERVICE_MEDIA)))
        self.assertEqual(_expected_media_count(), 8)

