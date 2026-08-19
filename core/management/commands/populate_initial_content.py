from django.core.management.base import BaseCommand

from core.content_defaults import (
    DEFAULT_EDUCATION,
    DEFAULT_HERO_METRICS,
    DEFAULT_PROJECTS,
    DEFAULT_SKILLS,
    DEFAULT_SOCIAL_LINKS,
)
from core.models import EducationItem, HeroMetric, Project, SocialLink, TechnicalSkill


class Command(BaseCommand):
    help = "Populate initial portfolio content (skills, education, projects, hero metrics, social links)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Clear existing data and repopulate",
        )

    def handle(self, *args, **options):
        force = options["force"]

        # Skills
        if force:
            TechnicalSkill.objects.all().delete()
            self.stdout.write("Cleared existing skills.")
        if not TechnicalSkill.objects.exists():
            for s in DEFAULT_SKILLS:
                TechnicalSkill.objects.create(**s)
            self.stdout.write(self.style.SUCCESS(f"Created {len(DEFAULT_SKILLS)} skills."))
        else:
            self.stdout.write("Skills already exist. Use --force to repopulate.")

        # Education
        if force:
            EducationItem.objects.all().delete()
            self.stdout.write("Cleared existing education items.")
        if not EducationItem.objects.exists():
            for e in DEFAULT_EDUCATION:
                EducationItem.objects.create(**e)
            self.stdout.write(self.style.SUCCESS(f"Created {len(DEFAULT_EDUCATION)} education items."))
        else:
            self.stdout.write("Education items already exist. Use --force to repopulate.")

        # Hero Metrics
        if force:
            HeroMetric.objects.all().delete()
            self.stdout.write("Cleared existing hero metrics.")
        if not HeroMetric.objects.exists():
            for m in DEFAULT_HERO_METRICS:
                HeroMetric.objects.create(**m)
            self.stdout.write(self.style.SUCCESS(f"Created {len(DEFAULT_HERO_METRICS)} hero metrics."))
        else:
            self.stdout.write("Hero metrics already exist. Use --force to repopulate.")

        # Social Links
        if force:
            SocialLink.objects.all().delete()
            self.stdout.write("Cleared existing social links.")
        if not SocialLink.objects.exists():
            for l in DEFAULT_SOCIAL_LINKS:
                SocialLink.objects.create(**l)
            self.stdout.write(self.style.SUCCESS(f"Created {len(DEFAULT_SOCIAL_LINKS)} social links."))
        else:
            self.stdout.write("Social links already exist. Use --force to repopulate.")

        # Projects
        if force:
            Project.objects.all().delete()
            self.stdout.write("Cleared existing projects.")
        if not Project.objects.exists():
            for p in DEFAULT_PROJECTS:
                Project.objects.create(**p)
            self.stdout.write(self.style.SUCCESS(f"Created {len(DEFAULT_PROJECTS)} projects."))
        else:
            self.stdout.write("Projects already exist. Use --force to repopulate.")

        self.stdout.write(self.style.SUCCESS("Done."))
