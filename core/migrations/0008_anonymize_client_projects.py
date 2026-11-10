"""Anonymize ArunaGo, LeadForge, and Juno names/slugs/text in existing rows.

Idempotent data migration. Does not delete projects or media files.
Re-run via: python manage.py anonymize_client_projects
"""

from django.db import migrations


def anonymize_forward(apps, schema_editor):
    from core.management.commands.anonymize_client_projects import (
        anonymize_client_projects,
    )

    anonymize_client_projects(apps, dry_run=False)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_profile_contact_links_and_cv"),
    ]

    operations = [
        migrations.RunPython(anonymize_forward, migrations.RunPython.noop),
    ]
