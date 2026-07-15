from django.core.management.base import BaseCommand

from core.content_defaults import (
    DEFAULT_PERSONA,
    DEFAULT_PHILOSOPHY,
    DEFAULT_PROJECTS,
    DEFAULT_SKILLS,
)
from core.models import PersonaSection, PhilosophyParagraph, Project, TechnicalSkill


class Command(BaseCommand):
    help = "Populate initial home page content (persona, philosophy, skills)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Replace existing persona, philosophy, and skills data.",
        )

    def handle(self, *args, **options):
        force = options["force"]

        persona, created = PersonaSection.objects.update_or_create(
            pk=1,
            defaults=DEFAULT_PERSONA,
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Persona section {'created' if created else 'updated'}: {persona.heading}"
            )
        )

        if force:
            PhilosophyParagraph.objects.all().delete()
            TechnicalSkill.objects.all().delete()
            Project.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared existing philosophy, skills, and projects."))

        philosophy_created = 0
        for index, content in enumerate(DEFAULT_PHILOSOPHY, start=1):
            _, created = PhilosophyParagraph.objects.update_or_create(
                order=index,
                defaults={"content": content, "is_active": True},
            )
            if created:
                philosophy_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Philosophy paragraphs ready ({philosophy_created} new, {len(DEFAULT_PHILOSOPHY)} total)."
            )
        )

        skills_created = 0
        for skill_data in DEFAULT_SKILLS:
            _, created = TechnicalSkill.objects.update_or_create(
                skill_id=skill_data["skill_id"],
                defaults={
                    "order": skill_data["order"],
                    "title": skill_data["title"],
                    "subtitle": skill_data["subtitle"],
                    "proficiency": skill_data["proficiency"],
                    "color": skill_data["color"],
                    "icon": skill_data["icon"],
                    "tags": skill_data["tags"],
                    "is_active": True,
                },
            )
            if created:
                skills_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Technical skills ready ({skills_created} new, {len(DEFAULT_SKILLS)} total)."
            )
        )

        projects_created = 0
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
                projects_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Projects ready ({projects_created} new, {len(DEFAULT_PROJECTS)} total)."
            )
        )
        self.stdout.write(self.style.SUCCESS("Initial home content populated successfully."))
