from django.db import migrations


def seed_forward(apps, schema_editor):
    from core.service_defaults import seed_services
    from core.service_media_seed import seed_service_media

    seed_services(apps, overwrite=False)
    seed_service_media(apps)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_seed_services"),
    ]

    operations = [
        migrations.RunPython(seed_forward, migrations.RunPython.noop),
    ]
