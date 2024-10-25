# Generated by Django 4.2.16 on 2024-10-06 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tcf_website", "0012_alter_review_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="Discipline",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="section",
            name="cost",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="course",
            name="disciplines",
            field=models.ManyToManyField(blank=True, to="tcf_website.discipline"),
        ),
    ]