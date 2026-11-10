import json

from django.apps import apps
from django.core.management import call_command
from django.test import TestCase

from core.content_defaults import DEFAULT_PROJECTS
from core.management.commands.anonymize_client_projects import (
    CLIENT_NAME_PATTERNS,
    PROJECT_RENAMES,
    anonymize_client_projects,
)
from core.models import Project, ProjectImage


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
