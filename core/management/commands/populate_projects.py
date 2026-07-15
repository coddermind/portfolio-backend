from django.core.management.base import BaseCommand

from core.content_defaults import DEFAULT_PROJECTS
from core.models import Project


class Command(BaseCommand):
    help = "Populate portfolio projects with Muhammad Abrar's AI automation project data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Delete all existing projects before seeding the default set.",
        )

    def handle(self, *args, **options):
        force = options["force"]

        if force:
            deleted_count, _ = Project.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f"Cleared {deleted_count} existing project record(s).")
            )

        created_count = 0
        updated_count = 0

        for project_data in DEFAULT_PROJECTS:
            _, created = Project.objects.update_or_create(
                slug=project_data["slug"],
                defaults={
                    "order": project_data["order"],
                    "title": project_data["title"],
                    "year": project_data["year"],
                    "short_description": project_data["short_description"],
                    "architectural_vision": project_data["architectural_vision"],
                    "tags": project_data["tags"],
                    "icon": project_data["icon"],
                    "color": project_data["color"],
                    "featured": project_data["featured"],
                    "timeline": project_data["timeline"],
                    "lead_role": project_data["lead_role"],
                    "environment": project_data["environment"],
                    "goal": project_data["goal"],
                    "result": project_data["result"],
                    "is_active": True,
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'}: {project_data['title']}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Projects ready — {created_count} created, {updated_count} updated, "
                f"{len(DEFAULT_PROJECTS)} total."
            )
        )
