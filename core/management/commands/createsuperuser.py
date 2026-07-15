import getpass
import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections

from core.utils import split_full_name

User = get_user_model()


class Command(BaseCommand):
    help = "Create a superuser with email, full name, and password."

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            dest="email",
            default=None,
            help="Superuser email address.",
        )
        parser.add_argument(
            "--full-name",
            dest="full_name",
            default=None,
            help="Superuser full name (split into first and last name).",
        )
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_true",
            dest="noinput",
            help="Run non-interactively using environment variables or flags.",
        )
        parser.add_argument(
            "--database",
            default=DEFAULT_DB_ALIAS,
            help='Nominates a database onto which to install the superuser.',
        )

    def handle(self, *args, **options):
        email = options.get("email")
        full_name = options.get("full_name")
        database = options["database"]
        verbosity = options["verbosity"]

        if options["noinput"]:
            email = email or os.environ.get("DJANGO_SUPERUSER_EMAIL")
            full_name = full_name or os.environ.get("DJANGO_SUPERUSER_FULL_NAME")
            password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
            if not email or not full_name or not password:
                raise CommandError(
                    "When using --noinput, provide --email, --full-name, and "
                    "DJANGO_SUPERUSER_PASSWORD (or set DJANGO_SUPERUSER_EMAIL, "
                    "DJANGO_SUPERUSER_FULL_NAME, DJANGO_SUPERUSER_PASSWORD)."
                )
        else:
            email = self._prompt_email(email)
            full_name = self._prompt_full_name(full_name)
            password = self._prompt_password()

        first_name, last_name = split_full_name(full_name)
        if not first_name:
            raise CommandError("Full name cannot be blank.")

        user_data = {
            "email": User.objects.normalize_email(email),
            "first_name": first_name,
            "last_name": last_name,
        }

        self.validate_password(password, user_data)

        with connections[database].cursor():
            if User.objects.using(database).filter(email=user_data["email"]).exists():
                raise CommandError("Error: That email is already taken.")

            User.objects.db_manager(database).create_superuser(
                email=user_data["email"],
                password=password,
                first_name=first_name,
                last_name=last_name,
            )

        if verbosity >= 1:
            self.stdout.write(self.style.SUCCESS("Superuser created successfully."))

    def _prompt_email(self, email):
        while not email:
            email = input("Email: ").strip()
            if not email:
                self.stderr.write("Error: Email cannot be blank.")
        return email

    def _prompt_full_name(self, full_name):
        while not full_name or not full_name.strip():
            full_name = input("Full name: ").strip()
            if not full_name:
                self.stderr.write("Error: Full name cannot be blank.")
        return full_name

    def _prompt_password(self):
        while True:
            password = getpass.getpass("Password: ")
            if not password:
                self.stderr.write("Error: Blank passwords aren't allowed.")
                continue
            password2 = getpass.getpass("Password (again): ")
            if password != password2:
                self.stderr.write("Error: Your passwords didn't match.")
                continue
            return password

    def validate_password(self, password, user_data):
        try:
            validate_password(password, User(**user_data))
        except exceptions.ValidationError as error:
            raise CommandError("\n".join(error.messages)) from error
