# Generated by Django 4.2.16 on 2024-11-21 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tcf_website", "0013_discipline_section_cost_course_disciplines"),
    ]

    operations = [
        migrations.CreateModel(
            name="SectionTime",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("days", models.CharField(max_length=20)),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "section",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tcf_website.section"
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(fields=["days"], name="tcf_website_days_cf23f5_idx"),
                    models.Index(
                        fields=["start_time", "end_time"], name="tcf_website_start_t_e19089_idx"
                    ),
                ],
            },
        ),
    ]
