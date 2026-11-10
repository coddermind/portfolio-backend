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
        self.assertGreaterEqual(len(DEFAULT_SERVICES), 6)

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

