from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_rename_challenge_solution_to_goal_result"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="contact_email",
            field=models.EmailField(blank=True, default="", max_length=254),
        ),
        migrations.AddField(
            model_name="profile",
            name="whatsapp_url",
            field=models.CharField(blank=True, default="", max_length=500),
        ),
        migrations.AddField(
            model_name="profile",
            name="github_url",
            field=models.CharField(blank=True, default="", max_length=500),
        ),
        migrations.AddField(
            model_name="profile",
            name="linkedin_url",
            field=models.CharField(blank=True, default="", max_length=500),
        ),
        migrations.AddField(
            model_name="profile",
            name="cv_file",
            field=models.FileField(blank=True, null=True, upload_to="cvs/"),
        ),
    ]
