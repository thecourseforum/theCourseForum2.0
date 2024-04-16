# Generated by Django 4.2.8 on 2024-01-24 21:30

from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations, models
from django.contrib.postgres.search import SearchVectorField



class Migration(migrations.Migration):

    dependencies = [
        ("tcf_website", "0009_remove_question_placeholder"),
    ]

    operations = [
        TrigramExtension(),
        migrations.AddField(
            model_name='course',
            name='search',
            field=SearchVectorField(null=True),
        )
    ]
