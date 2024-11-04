# Generated by Django 4.2.13 on 2024-11-03 20:52

import django.contrib.postgres.indexes
from django.db import migrations, models


def populate_full_name(apps, schema_editor):
    Instructor = apps.get_model("tcf_website", "Instructor")
    for instructor in Instructor.objects.all():
        instructor.full_name = f"{instructor.first_name} {instructor.last_name}".strip()
        instructor.save()


def populate_combined_mnemonic_number(apps, schema_editor):
    Course = apps.get_model("tcf_website", "Course")
    for course in Course.objects.all():
        course.combined_mnemonic_number = f"{course.subdepartment.mnemonic} {course.number}".strip()
        course.save()


class Migration(migrations.Migration):

    dependencies = [
        ("tcf_website", "0014_remove_instructor_website"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="course",
            name="tcf_website_subdepa_f296bc_idx",
        ),
        migrations.AddField(
            model_name="course",
            name="combined_mnemonic_number",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="instructor",
            name="full_name",
            field=models.CharField(blank=True, editable=False, max_length=511),
        ),
        migrations.AddIndex(
            model_name="course",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["combined_mnemonic_number"],
                name="course_mnemonic_number",
                opclasses=["gin_trgm_ops"],
            ),
        ),
        migrations.AddIndex(
            model_name="instructor",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["first_name"], name="first_name_instructor", opclasses=["gin_trgm_ops"]
            ),
        ),
        migrations.AddIndex(
            model_name="instructor",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["last_name"], name="last_name_instructor", opclasses=["gin_trgm_ops"]
            ),
        ),
        migrations.AddIndex(
            model_name="instructor",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["full_name"], name="full_name_instructor", opclasses=["gin_trgm_ops"]
            ),
        ),
        migrations.RunPython(populate_full_name),
        migrations.RunPython(populate_combined_mnemonic_number),
    ]
