from django.db import migrations


def seed_forward(apps, schema_editor):
    from core.service_defaults import seed_services

    seed_services(apps)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_service"),
    ]

    operations = [
        migrations.RunPython(seed_forward, migrations.RunPython.noop),
    ]
