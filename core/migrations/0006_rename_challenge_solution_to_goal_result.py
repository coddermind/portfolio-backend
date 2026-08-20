from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_contactmessage_educationitem_herometric_sociallink_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="project",
            old_name="challenge",
            new_name="goal",
        ),
        migrations.RenameField(
            model_name="project",
            old_name="solution",
            new_name="result",
        ),
    ]
