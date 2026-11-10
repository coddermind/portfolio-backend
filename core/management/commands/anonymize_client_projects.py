"""Anonymize employer client project names in the database.

Idempotent. Does not delete rows or media files. Safe to re-run.

Old client names (ArunaGo / LeadForge / Juno) are matched here and in the
accompanying data migration only.
"""

from __future__ import annotations

import re

from django.core.management.base import BaseCommand

# Ordered longest-first so "LeadForge AI" is rewritten before "LeadForge".
TEXT_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"aruna\s*go\s+ai\s+agent", re.IGNORECASE), "AI Operations Copilot"),
    (re.compile(r"aruna\s*go\s+admin", re.IGNORECASE), "the host platform admin"),
    (re.compile(r"aruna\s*go", re.IGNORECASE), "the operations platform"),
    (re.compile(r"\baruna\b", re.IGNORECASE), "the operations platform"),
    (re.compile(r"lead\s*forge[-\s]?ai", re.IGNORECASE), "AI Lead Generation Platform"),
    (re.compile(r"lead\s*forge", re.IGNORECASE), "AI Lead Generation Platform"),
    (
        re.compile(r"juno\s+seo\s+integration", re.IGNORECASE),
        "AI SEO Platform integration",
    ),
    (re.compile(r"juno\s+seo\s+agent", re.IGNORECASE), "AI SEO Platform"),
    (re.compile(r"juno\s+seo", re.IGNORECASE), "AI SEO Platform"),
    (re.compile(r"\bjuno\b", re.IGNORECASE), "AI SEO Platform"),
]

CLIENT_NAME_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"arunago", re.IGNORECASE),
    re.compile(r"aruna\s*go", re.IGNORECASE),
    re.compile(r"\baruna\b", re.IGNORECASE),
    re.compile(r"lead\s*forge", re.IGNORECASE),
    re.compile(r"leadforge", re.IGNORECASE),
    re.compile(r"\bjuno\b", re.IGNORECASE),
]

PROJECT_RENAMES: list[dict] = [
    {
        "old_slugs": ("arunago-ai-agent", "aruna-go-ai-agent", "arunago"),
        "title_needles": ("arunago", "aruna go", "aruna"),
        "new_slug": "ai-operations-copilot",
        "new_title": "AI Operations Copilot",
    },
    {
        "old_slugs": ("leadforge-ai", "lead-forge-ai", "leadforge", "lead-forge"),
        "title_needles": ("leadforge", "lead forge"),
        "new_slug": "ai-lead-generation-platform",
        "new_title": "AI Lead Generation Platform",
    },
    {
        "old_slugs": ("juno-seo-agent", "juno-seo", "juno"),
        "title_needles": ("juno seo", "juno"),
        "new_slug": "ai-seo-platform",
        "new_title": "AI SEO Platform",
    },
]

TEXT_FIELDS = (
    "title",
    "slug",
    "short_description",
    "full_description",
    "goal",
    "result",
)
JSON_FIELDS = ("tags", "architecture", "pipeline_steps", "metrics")


def apply_text_replacements(value: str) -> str:
    updated = value
    for pattern, replacement in TEXT_REPLACEMENTS:
        updated = pattern.sub(replacement, updated)
    return updated


def rewrite_value(value):
    if isinstance(value, str):
        return apply_text_replacements(value)
    if isinstance(value, list):
        return [rewrite_value(item) for item in value]
    if isinstance(value, dict):
        return {key: rewrite_value(item) for key, item in value.items()}
    return value


def _contains_client_name(value: str) -> bool:
    return any(pattern.search(value) for pattern in CLIENT_NAME_PATTERNS)


def _find_matching_projects(Project, spec: dict):
    matches = []
    seen_pks = set()
    queryset = Project.objects.all()
    old_slugs = {slug.lower() for slug in spec["old_slugs"]}
    new_slug = spec["new_slug"].lower()

    for project in queryset:
        slug = (project.slug or "").lower()
        title = project.title or ""
        matched = slug in old_slugs or slug == new_slug
        if not matched:
            title_lower = title.lower()
            matched = any(needle in title_lower for needle in spec["title_needles"])
        if matched and project.pk not in seen_pks:
            seen_pks.add(project.pk)
            matches.append(project)
    return matches


def _rewrite_project_fields(project) -> bool:
    changed = False
    for field in TEXT_FIELDS:
        if field == "slug":
            continue
        current = getattr(project, field, "") or ""
        updated = apply_text_replacements(current)
        if updated != current:
            setattr(project, field, updated)
            changed = True
    for field in JSON_FIELDS:
        current = getattr(project, field, None)
        updated = rewrite_value(current)
        if updated != current:
            setattr(project, field, updated)
            changed = True
    return changed


def anonymize_client_projects(apps, dry_run: bool = False) -> list[str]:
    """Rewrite client project names/slugs/text. Returns a log of actions."""
    Project = apps.get_model("core", "Project")
    ProjectImage = apps.get_model("core", "ProjectImage")
    actions: list[str] = []

    taken_slugs = {
        (project.slug or "").lower()
        for project in Project.objects.all()
    }

    for spec in PROJECT_RENAMES:
        matches = _find_matching_projects(Project, spec)
        if not matches:
            actions.append(
                f"No database row matched {spec['new_title']} "
                f"(looked for slugs {list(spec['old_slugs'])})."
            )
            continue

        for project in matches:
            original_slug = project.slug
            original_title = project.title
            field_changed = _rewrite_project_fields(project)

            if project.title != spec["new_title"]:
                project.title = spec["new_title"]
                field_changed = True

            desired_slug = spec["new_slug"]
            slug_taken_by_other = (
                desired_slug.lower() in taken_slugs
                and (original_slug or "").lower() != desired_slug.lower()
            )
            if (original_slug or "").lower() != desired_slug.lower():
                if slug_taken_by_other:
                    actions.append(
                        f"Kept slug {original_slug!r} for {original_title!r}: "
                        f"{desired_slug!r} is already used by another project."
                    )
                else:
                    taken_slugs.discard((original_slug or "").lower())
                    project.slug = desired_slug
                    taken_slugs.add(desired_slug.lower())
                    field_changed = True

            image_changes = 0
            for image in ProjectImage.objects.filter(project_id=project.pk):
                alt = image.alt_text or ""
                new_alt = apply_text_replacements(alt)
                if new_alt != alt:
                    image.alt_text = new_alt
                    image_changes += 1
                    if not dry_run:
                        image.save(update_fields=["alt_text"])

            if field_changed or image_changes:
                if not dry_run:
                    project.save()
                actions.append(
                    f"{'Would update' if dry_run else 'Updated'} "
                    f"{original_title!r} ({original_slug!r}) → "
                    f"{project.title!r} ({project.slug!r})"
                    + (f", {image_changes} image alt text(s)" if image_changes else "")
                )
            else:
                actions.append(
                    f"Already anonymized: {project.title!r} ({project.slug!r})"
                )

    # Scrub leftover client-name strings on any other project (e.g. tags).
    matched_pks = set()
    for spec in PROJECT_RENAMES:
        for project in _find_matching_projects(Project, spec):
            matched_pks.add(project.pk)

    for project in Project.objects.all():
        if project.pk in matched_pks:
            continue
        field_changed = _rewrite_project_fields(project)
        if field_changed:
            if not dry_run:
                project.save()
            actions.append(
                f"{'Would scrub' if dry_run else 'Scrubbed'} leftover client names "
                f"on {project.title!r} ({project.slug!r})"
            )

    return actions


class Command(BaseCommand):
    help = (
        "Anonymize ArunaGo, LeadForge, and Juno project names, slugs, and "
        "related text in the database. Idempotent; does not delete data."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print the planned updates without writing to the database.",
        )

    def handle(self, *args, **options):
        from django.apps import apps

        dry_run = options["dry_run"]
        actions = anonymize_client_projects(apps, dry_run=dry_run)
        for line in actions:
            self.stdout.write(line)
        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run — no changes saved."))
        else:
            self.stdout.write(self.style.SUCCESS("Client project anonymization complete."))
